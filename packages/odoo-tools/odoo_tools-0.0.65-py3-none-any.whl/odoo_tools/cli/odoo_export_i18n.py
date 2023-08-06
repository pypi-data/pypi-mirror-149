import sys
from itertools import groupby
from optparse import OptionParser
from logging import getLogger
from io import StringIO
from ..compat import Path
from ..modules.search import find_modules_paths
from ..modules.translate import PoFileWriter, PoFileReader
import six

_logger = getLogger(__name__)


def get_parser():
    parser = OptionParser()

    parser.add_option(
        '-c',
        '--config',
        dest='config',
        help='path to config file',
    )

    parser.add_option(
        '-d',
        '--database',
        dest='database',
        help="Which Database to use to export translation",
    )

    parser.add_option(
        '-l',
        '--languages',
        dest="languages",
        help="CSV of languages to export"
    )

    parser.add_option(
        '-m',
        '--modules',
        dest="modules",
        help="Modules to export"
    )

    parser.add_option(
        '-p',
        '--paths',
        dest='paths',
        help="CSV of paths to export files into",
    )

    parser.add_option(
        '--with-pot',
        dest="with_pot",
        action="store_true",
        default=False,
        help="Generate POT file"
    )

    return parser


def get_key(key_id):
    def wrap(value):
        return value[key_id]
    return wrap


def get_filename(language, module):
    if language:
        try:
            family, dialect = language.lower().split('_')
            if family == dialect:
                language = family
        except Exception:
            pass

    filename = (
        '{}.po'.format(language)
        if language
        else '{}.pot'.format(module)
    )
    return filename


def export_translation(database, languages, modules):
    """
    Export terms grouped by module
    """
    import odoo
    from odoo.modules.registry import Registry

    # TODO create a unified term exporter. The one from Odoo14 is
    # much better than previous versions. It could be a good start
    # as resources don't need to have odoo access.
    # Then implement a loader that can extract terms from fields
    # like Selection and translatable fields.
    #
    # Odoo14 implement selections through ir.models.fields.selection
    # while previous versions use the field.selection attribute.
    #
    # We don't really have to complicate ourselves as in odoo14
    # It's just a basic model being exported (need to guess proper xmlid)
    # While on earlier versions of odoo we can simply use a custom loader
    # for selection field.
    # In practice we could attempt to export translations using both format
    # and odoo should simply ignore older formats and everyone is happy.
    try:
        # Odoo 10, 11, 12, 13
        from odoo.tools import trans_generate
    except ImportError:
        # Odoo 14
        from odoo.tools.translate import TranslationModuleReader

        def trans_generate(language, modules, cr):
            reader = TranslationModuleReader(
                cr,
                modules=modules,
                lang=language
            )
            return [
                x
                for x in reader
            ]

    registry = Registry.new(database)
    with odoo.api.Environment.manage():
        with registry.cursor() as cr:
            for language in languages:

                translations = trans_generate(
                    language,
                    modules,
                    cr
                )

                translations.sort()

                for module, terms in groupby(translations, key=get_key(0)):
                    yield language, module, terms

    _logger.info('translation file written successfully')


def command():
    parser = get_parser()

    (options, args) = parser.parse_args()

    try:
        import odoo
        from odoo.tools import config
    except ImportError:
        print("Couldn't import odoo package, please install odoo")
        sys.exit(1)

    config_args = []

    if options.config:
        config_args.append('-c')
        config_args.append(options.config)

    if options.database:
        config_args.append('-d')
        config_args.append(options.database)

    if options.paths:
        config_args.append('--addons-path')
        config_args.append(",".join([
            str(Path.cwd() / path)
            for path in options.paths.split(',')
        ]))

    config.parse_config(config_args)

    languages = []

    if options.languages:
        languages += [
            lang.strip()
            for lang in options.languages.split(',')
        ]

    if options.with_pot:
        languages.append(None)

    paths = [
        path.strip()
        for path in options.paths.split(',')
    ]

    modules = find_modules_paths(paths, set())

    modules_by_name = {
        module.technical_name: module
        for module in modules
    }

    for language, module, rows in export_translation(
        options.database,
        languages,
        [module.strip() for module in options.modules.split(',')]
    ):
        # For all languages including pot file
        module_path = modules_by_name[module].path
        filename = get_filename(language, module)
        trans_path = module_path / 'i18n' / filename
        trans_path.parent.mkdir(parents=True, exist_ok=True)

        _logger.info(
            "Exporting translation %s.%s to %s",
            module,
            language,
            trans_path
        )

        if trans_path.exists():
            origin_po_file = PoFileReader(trans_path.open('rb'))
        else:
            with trans_path.open("w+") as buffer:
                buffer.write("")

            with trans_path.open('rb') as buffer:
                origin_po_file = PoFileReader(buffer)

        with trans_path.open('wb+') as buffer:
            po_writer = PoFileWriter(
                buffer,
                language,
                pofile=origin_po_file.pofile
            )

            for module, type, name, res_id, source, value, comments in rows:

                po_writer.add_entry(
                    modules=[module],
                    tnrs=[
                        (type, name, res_id)
                    ],
                    source=source,
                    trad=value,
                    comments=comments
                )

            po_writer.write()
