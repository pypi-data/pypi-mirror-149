from itertools import chain
from giturlparse import parse, GitUrlParsed


def git_to_path(value):
    if isinstance(value, GitUrlParsed):
        parsed = value
    else:
        parsed = parse(value)

    return "{}_{}".format(
        parsed.owner,
        parsed.repo
    )


def get_services(services):
    return {
        service.get('name'): service
        for service in services.get('services')
    }


#    def addons_by_project(options, addons):
#        res = {}
# 
#        for addon in addons:
#            if addon['url'] == 'self':
#                if options.ignore_self:
#                    continue
#                parsed = parse(options.url)
#            else:
#                if isinstance(addon['url'], str):
#                    parsed = parse(addon['url'])
#                else:
#                    parsed = addon['url']
# 
#            res[parsed.repo] = dict(
#                addon,
#                url=parsed,
#            )
# 
#        return res
# 
# 
#    def merge_addons(options, base, other):
#        base_addons = addons_by_project(options, base)
#        other_addons = addons_by_project(options, other)
# 
#        for name, addon in other_addons.items():
#            if name not in base_addons:
#                base_addons[name] = addon
#            else:
#                base_addons[name] = dict(base_addons[name], **addon)
# 
#        return [
#            addon
#            for addon in base_addons.values()
#        ]
# 
# 
#    def merge_services(options, base, other):
#        basic_inherit = dict(base, **other)
# 
#        if base.get('addons') or other.get('addons'):
#            basic_inherit['addons'] = merge_addons(
#                options,
#                base.get('addons', []),
#                other.get('addons', [])
#            )
# 
#        return basic_inherit


class Addons(list):
    pass


def merge_dict(dict1, dict2):
    res = {}

    dict1 = dict1 or {}
    dict2 = dict2 or {}

    for key in chain(dict1.keys(), dict2.keys()):
        if key in dict1:
            val_type1 = dict1.get(key)
        else:
            val_type1 = None

        if key in dict2:
            val_type2 = dict2.get(key)
        else:
            val_type2 = None

        if isinstance(val_type2, dict):
            res[key] = merge_dict(val_type1 or {}, val_type2)
            continue

        if isinstance(val_type2, Addons):
            result = Addons()
            # urls = set()

            by_url = {}

            for addon in val_type2:
                new_addon = addon.copy()
                by_url[addon.get('url').url] = new_addon

            for addon in (val_type1 or []):
                new_addon = addon.copy()

                if addon.get('url').url in by_url:
                    by_url[addon.get('url').url] = merge_dict(
                        new_addon,
                        by_url[addon.get('url').url],
                    )
                else:
                    by_url[addon.get('url').url] = new_addon

            for addon in by_url.values():
                result.append(addon)

            res[key] = result
            continue

        if isinstance(val_type2, list):
            res[key] = [
                addon
                for addon in chain(val_type1 or [], val_type2)
            ]
            continue

        if val_type1 is not None:
            res[key] = val_type1
        else:
            res[key] = val_type2

    return res


class Service(object):
    def __init__(self, data=None):
        if data is None:
            data = {}
        self.data = data

    def copy(self):
        new_data = self.data.copy()
        return Service(new_data)


class Normalizer(object):

    def __init__(
        self,
        resolve_inheritance=None,
        inherit_addons=None,
        self_url=None,
        ignore_self=False,
    ):
        self.value = None
        self.resolve_inheritance = resolve_inheritance
        self.inherit_addons = inherit_addons
        self.ignore_self = ignore_self
        if self_url:
            self.self_url = self_url
        else:
            self.self_url = 'git@gitlab.com:archeti/${odoo:project}.git'

    def parse(self, value):
        self.normalize_config(value)
        return self.value

    def normalize_url(self, url):
        if url == 'self':
            self.value = parse(self.self_url)
        else:
            self.value = parse(url)

    def normalize_addon(self, addon):
        self.normalize_url(addon.get('url'))
        url = self.value
        self.value = dict(addon, url=url)

    def normalize_addons(self, addons):
        normalized_addons = Addons()

        for addon in addons:
            if addon.get('url') == 'self' and self.ignore_self:
                continue
            self.normalize_addon(addon)
            normalized_addons.append(self.value)

        self.value = normalized_addons

    def normalize_kv(self, kv):
        if isinstance(kv, dict):
            self.value = kv.copy()
            return
        if isinstance(kv, list):
            self.value = {
                elem['key']: elem['value']
                for elem in kv
            }
            return

    def normalize_service(self, service, services=None):
        self.normalize_addons(service.get('addons', []))
        addons = self.value

        self.normalize_kv(service.get('env', {}))
        env = self.value

        self.normalize_kv(service.get('labels', {}))
        labels = self.value

        normalized_service = dict(
            service,
            addons=addons,
            env=env,
            labels=labels
        )

        if (
            normalized_service.get('inherit') and
            self.resolve_inheritance
        ):
            base_service_name = normalized_service.get('inherit')

            for found_service in services:
                if found_service.get('name') == base_service_name:
                    break
            else:
                found_service = None

            if found_service:
                self.normalize_service(found_service, services)
                base_service = self.value

                if not self.inherit_addons:
                    del base_service['addons']
                else:
                    del normalized_service['inherit']

                child_service = normalized_service

                normalized_service = merge_dict(
                    normalized_service,
                    base_service,
                )

                normalized_service['name'] = child_service['name']

        self.value = normalized_service

    def normalize_services(self, services):
        normalized_services = []

        for service in services:
            self.normalize_service(service, services=services)
            normalized_services.append(self.value)

        self.value = normalized_services

    def normalize_config(self, config):
        self.normalize_services(config.get('services', []))
        services = self.value

        self.value = dict(
            config,
            services=services
        )
