#!/usr/bin/env python3
"""审计 Skill 外置配置；默认只读，删除必须显式选文件、备份并确认。"""
import argparse
import json
import os
import shutil
import stat
import sys
from pathlib import Path

DEFAULT_REGISTRY = Path(__file__).resolve().parent.parent / 'references' / 'config-registry.json'


def config_root(value):
    if value:
        return Path(value).expanduser()
    base = os.environ.get('XDG_CONFIG_HOME')
    if base and Path(base).is_absolute():
        return Path(base) / 'aster-xu-lab'
    return Path.home() / '.config' / 'aster-xu-lab'


def resolve_root(value):
    root = config_root(value)
    if not root.exists():
        raise ValueError(f'配置目录不存在：{root}')
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f'配置目录必须是普通目录：{root}')
    return root.resolve()


def load_registry(path):
    path = Path(path).expanduser()
    data = json.loads(path.read_text(encoding='utf-8'))
    skills = data.get('skills')
    if not isinstance(skills, dict) or not skills:
        raise ValueError('配置注册表缺少非空 skills 对象')
    by_file = {}
    for skill, entry in skills.items():
        if not isinstance(entry, dict) or not entry.get('file'):
            raise ValueError(f'配置注册表条目无效：{skill}')
        item = dict(entry)
        item['skill'] = skill
        by_file[item['file']] = item
    return by_file, path


def safe_name(name):
    return bool(name) and Path(name).name == name and name not in ('.', '..') and '\\' not in name


def inspect(path, entry, installed_root):
    result = path.lstat()
    info = {
        'name': path.name,
        'path': str(path),
        'size': result.st_size,
        'mode': f'{stat.S_IMODE(result.st_mode):o}',
        'symlink': path.is_symlink(),
        'registered': entry is not None,
    }
    if os.name != 'nt':
        info['permission_warning'] = info['mode'] != '600'
    if path.is_symlink():
        info['status'] = 'symlink'
        info['reason'] = '软链配置不自动处理；先确认 dotfiles 归属'
        return info
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        info['status'] = 'invalid'
        info['reason'] = f'JSON 无法解析：{type(exc).__name__}'
        return info
    info['valid_json'] = True
    schema = data.get('schema_version', data.get('version')) if isinstance(data, dict) else None
    info['schema_version'] = schema
    if entry is None:
        info['status'] = 'unknown'
        info['reason'] = '未在配置注册表中登记；不自动处理'
        return info
    info['skill'] = entry['skill']
    expected = entry.get('schema_version')
    if expected is not None and schema != expected:
        info['status'] = 'schema-mismatch'
        info['reason'] = f'schema_version={schema!r}，注册表期望 {expected!r}'
        return info
    if installed_root is None or not Path(installed_root).is_dir():
        info['status'] = 'ok'
        info['reason'] = '已登记；未检测到安装目录，未判断是否孤立'
        return info
    info['installed'] = (Path(installed_root) / entry['skill']).is_dir()
    if not info['installed']:
        info['status'] = 'orphan'
        info['reason'] = '已登记但未检测到安装；可能是卸载后残留'
        return info
    info['status'] = 'ok'
    info['reason'] = '已登记且检测到安装'
    return info


def summary(results):
    counts = {}
    for item in results:
        counts[item['status']] = counts.get(item['status'], 0) + 1
    return {
        'total': len(results),
        'by_status': counts,
        'permission_warnings': sum(1 for item in results if item.get('permission_warning')),
    }


def audit(root, by_file, installed_root):
    return [inspect(path, by_file.get(path.name), installed_root)
            for path in sorted(root.glob('*.json'))]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', help='配置目录；默认按平台解析')
    parser.add_argument('--registry', default=str(DEFAULT_REGISTRY), help='配置注册表 JSON')
    parser.add_argument('--installed-root', help='已安装 Skill 目录；不传则该次审计不检查安装状态')
    parser.add_argument('--json', action='store_true', help='输出 JSON')
    parser.add_argument('--archive-dir', help='删除前归档目录')
    parser.add_argument('--delete', action='store_true', help='删除显式指定的配置文件')
    parser.add_argument('--file', action='append', default=[], help='要删除的文件名，可重复')
    parser.add_argument('--yes', action='store_true', help='确认删除')
    parser.add_argument('--force', action='store_true', help='允许删除已安装 Skill 的配置')
    args = parser.parse_args()

    try:
        root = resolve_root(args.root)
        by_file, registry_path = load_registry(args.registry)
        installed_root = Path(args.installed_root).expanduser() if args.installed_root else None
        results = audit(root, by_file, installed_root)
        deleted = []
        if args.delete:
            if not args.yes:
                raise ValueError('删除需要 --yes 明确确认')
            if not args.file:
                raise ValueError('删除需要 --file 指定文件名')
            if not args.archive_dir:
                raise ValueError('删除需要 --archive-dir 保存备份')
            archive_root = Path(args.archive_dir).expanduser()
            for name in args.file:
                if not safe_name(name):
                    raise ValueError(f'文件名不安全：{name!r}')
                item = next((row for row in results if row['name'] == name), None)
                if item is None:
                    raise ValueError(f'文件不在审计结果中：{name}')
                if item['status'] == 'symlink':
                    raise ValueError(f'拒绝自动删除软链配置：{name}')
                if item['status'] == 'ok' and not args.force:
                    raise ValueError(f'拒绝删除已安装 Skill 的配置：{name}；如确认，加 --force')
                source = root / name
                if source.is_symlink() or source.resolve().parent != root:
                    raise ValueError(f'文件越出配置目录：{name}')
                archive_root.mkdir(parents=True, exist_ok=True)
                target = archive_root / name
                if target.exists():
                    raise ValueError(f'归档目标已存在：{target}')
                shutil.move(str(source), str(target))
                deleted.append({'name': name, 'status': item['status'], 'archive': str(target)})
            results = audit(root, by_file, installed_root)
        report = {
            'root': str(root),
            'registry': str(registry_path),
            'installed_root': str(installed_root) if installed_root else None,
            'files': results,
            'summary': summary(results),
            'deleted': deleted,
        }
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(f'配置目录：{root}')
            print(f'注册表：{registry_path}')
            print(f"安装目录：{installed_root if installed_root else '未检查'}")
            for item in results:
                warning = ' 权限不是 0600' if item.get('permission_warning') else ''
                print(f"{item['name']}\t{item['status']}\t{item['mode']}\t{item['reason']}{warning}")
            for item in deleted:
                print(f"已归档：{item['name']} -> {item['archive']}")
            counts = report['summary']['by_status']
            print('汇总：' + ', '.join(f'{key}={value}' for key, value in sorted(counts.items())))
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f'配置审计失败：{exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
