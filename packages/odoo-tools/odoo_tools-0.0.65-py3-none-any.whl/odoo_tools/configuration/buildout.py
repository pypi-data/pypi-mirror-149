buildout_template = """[buildout]
extends = base.cfg
"""

base_template = """[{name}]
{odoo_repo}
{project_name}
{version}
{addons}
{options}
"""

version_template = """
version = git {repo} ../../../../git/odoo ${{odoo:odoo_branch}}
"""

base_repo = "https://github.com/odoo/odoo.git"


def format_options(options):
    parts = []
    option_template = "options.{key} = {value}"

    for key, value in options.items():
        parts.append(
            option_template.format(
                key=key,
                value=value
            )
        )

    return "\n".join(parts)


def format_addons(service, default_branch=None, project=None):
    addons = service.get('addons', [])

    if not addons:
        return ""

    addon_line = "git {url} ../../{project} {ref}"

    prepend_text = (
        "addons = "
        if 'inherit' not in service
        else "addons += "
    )
    separator = "\n" + " " * len(prepend_text)

    parts = []

    for addon in addons:
        url = addon['url']

        ref = (
            addon.get('branch') or
            addon.get('commit') or
            default_branch or
            "${odoo:branch}"
        )

        parts.append(addon_line.format(
            url=url.url,
            project=url.repo,
            ref=ref
        ))

    return "{}{}\n".format(prepend_text, separator.join(parts))


def to_buildout(service, default_branch=None):
    template = base_template

    odoo_config = service.get('odoo', {})
    odoo_repo_dict = odoo_config.get('repo', {})
    options_dict = odoo_config.get('options', {})

    odoo_repo = (
        version_template.format(
            repo=odoo_repo_dict['url']
        )
        if 'url' in odoo_repo_dict
        else ""
    )

    odoo_version = (
        odoo_repo_dict.get('commit') or
        odoo_repo_dict.get('branch') or
        odoo_config.get('version') or
        default_branch or
        ""
    )
    version_line = (
        "odoo_branch = {}".format(odoo_version)
        if odoo_version else ""
    )

    project = odoo_config.get('project')
    project_line = (
        "project = {}".format(project)
        if project else ""
    )

    addons = format_addons(service, default_branch, project)
    options = format_options(options_dict)

    parts = []

    parts.append(template.format(
        name=service.get('name'),
        project_name=project_line,
        addons=addons,
        options=options,
        version=version_line,
        odoo_repo=odoo_repo,
    ))

    return parts


def to_buildout_cfg(services, branch, env=None):
    parts = [buildout_template]

    if not env:
        for key, values in services.items():
            parts += to_buildout(values, branch)
    else:
        parts += to_buildout(services[env], branch)

    return parts
