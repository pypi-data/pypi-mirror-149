import warnings
from dataclasses import dataclass, is_dataclass, field
from typing import Optional, Dict

from borax.system import load_class
from django.apps import apps
from typing_extensions import Literal

from .dms import DependencyManager
from .tms import Theme, parse_theme_label, ThemeManager


@dataclass
class DJEOpts:
    echarts_version: str = '4.8.0'
    dms_repo: str = 'pyecharts'
    dep2url: Dict[str, str] = field(default_factory=dict)
    local_dir: str = ''

    renderer: Literal['svg', 'canvas'] = 'canvas'
    echarts_theme: Optional[str] = None

    theme_name: Optional[str] = None
    theme_app: Optional[str] = None
    theme_d2u: Optional[Dict] = None
    site_class: Optional[str] = None

    baidu_map_ak: str = None

    def get_echarts_theme(self, instance_theme) -> str:
        if self.echarts_theme:
            return self.echarts_theme
        else:
            return instance_theme

    @staticmethod
    def upgrade_dict(vals: dict):
        def _u(_old, _new=None):
            val = vals.pop(_old, None)
            if val:
                warnings.warn(f'Option {_old} is deprecated. Use {_new} instead.', DeprecationWarning)
                if _new is not None and _new not in vals:
                    vals[_new] = val

        _u('map_js_host')
        _u('map_repo')
        _u('lib_js_host', 'dms_repo')
        _u('lib_repo', 'dms_repo')
        _u('local_host', 'local_dir')
        _u('file2map', 'dep2url')

        return vals


_THEME_NAME2APP_ = {
    'bootstrap3': 'django_echarts.contrib.bootstrap3',
    'bootstrap5': 'django_echarts.contrib.bootstrap5',
    'material': 'django_echarts.contrib.material'
}


# SettingsStore -> DependencyManage -> DJEOpts
class SettingsStore:
    """A settings entry for dms and tms."""

    def __init__(self, *, echarts_settings=None, extra_settings=None, **kwargs):
        # Pre check settings

        self._extra_settings = extra_settings or {}
        self.static_url = kwargs.get('static_url', '/static/')
        self.staticfiles_dir = kwargs.get('staticfiles_dir', '')

        if isinstance(echarts_settings, dict):
            new_opts = DJEOpts.upgrade_dict(echarts_settings)
            self._opts = DJEOpts(**new_opts)
        elif isinstance(echarts_settings, DJEOpts):
            self._opts = echarts_settings
        elif is_dataclass(echarts_settings):
            self._opts = echarts_settings()
        else:
            self._opts = DJEOpts()

        context = {
            'echarts_version': self._opts.echarts_version,
            'baidu_map_ak': self._opts.baidu_map_ak
        }
        if 'STATIC_URL' in self._extra_settings:
            context.update({'STATIC_URL': self.static_url})
        self._dms = DependencyManager.create_default(
            context=context,
            repo_name=self._opts.dms_repo
        )
        self._dms.load_from_dep2url_dict(self._opts.dep2url)
        self._dms.set_localize_opts(static_url=self.static_url, staticfiles_dir=self.staticfiles_dir)

        user_theme_label, user_theme_app = self._auto_get_theme_params()
        if not self._opts.theme_app:
            self._opts.theme_app = user_theme_app
        self._tms = ThemeManager.create_from_module(theme_app=user_theme_app, d2u=self._opts.theme_d2u)
        self._tms.set_localize_opts(static_url=self.static_url, staticfiles_dir=self.staticfiles_dir)

        self._theme = self._tms.create_theme(user_theme_label)

    # #### Public API: Generate js link using current configure ########

    @property
    def opts(self) -> DJEOpts:
        return self._opts

    @property
    def dependency_manager(self) -> DependencyManager:
        return self._dms

    @property
    def theme_manger(self) -> ThemeManager:
        return self._tms

    @property
    def theme(self) -> Theme:
        return self._theme

    def resolve_url(self, dep_name: str, repo_name: Optional[str] = None) -> str:
        return self._dms.resolve_url(dep_name, repo_name)

    def generate_js_link(self, js_name, js_host=None, **kwargs):
        warnings.warn('The method SettingsStore.generate_js_link is deprecated, use SettingsStore.resolve_url instead.',
                      DeprecationWarning, stacklevel=2)
        return self._dms.resolve_url(dep_name=js_name, repo_name=js_host)

    def get_site_obj(self):
        if not self._opts.site_class:
            raise TypeError('The settings DJANGO_ECHARTS.site_class is required for this feature.')
        return load_class(self._opts.site_class)

    def switch_palette(self, theme_label: str) -> Theme:
        self._theme = self._tms.create_theme(theme_label)
        return self._theme

    def _auto_get_theme_params(self):
        """Get theme from settings.INSTALLED_APPS.A django project environment is required."""
        theme_app = ''
        for app_config in apps.get_app_configs():
            if app_config.name == self._opts.theme_app or app_config.name in _THEME_NAME2APP_.values():
                theme_app = app_config.name
                break
        if not theme_app:
            raise ValueError('theme_app value is not set.')

        name_from_app = theme_app.split('.')[-1]

        if self._opts.theme_name:
            _, name_from_cfg, _, _ = parse_theme_label(self._opts.theme_name)
            if name_from_cfg != name_from_app:
                raise ValueError(f'theme_app={name_from_app} is not same with theme_name={name_from_cfg}')
            theme_label = self._opts.theme_name
        else:
            theme_label = name_from_app
        return theme_label, theme_app

    def create_theme(self, theme_label: str = None) -> Theme:
        if not theme_label:
            return self._theme
        theme_palette, theme_name, palette, is_local = parse_theme_label(theme_label)
        if self._opts.theme_app:
            theme_app = self._opts.theme_app
        else:
            theme_app = _THEME_NAME2APP_.get(theme_name)
        return self._tms.create_theme(theme_label, theme_app)
