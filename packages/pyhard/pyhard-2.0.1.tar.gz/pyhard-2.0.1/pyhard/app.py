import io
from dataclasses import dataclass, field
from numbers import Number
from pathlib import Path
from typing import Any, List, Union, Tuple

import holoviews as hv
import numpy as np
import pandas as pd
import panel as pn
import plotly.express as px
from bokeh.core.enums import MarkerType
from bokeh.models import HoverTool
from bokeh.settings import settings
from holoviews import opts, dim
from holoviews.streams import PlotReset, SelectionExpr
from shapely.geometry import Point, MultiPoint, Polygon, MultiPolygon
from sklearn.decomposition import PCA

from pyhard.context import Workspace

_my_path = Path(__file__).parent

settings.resources = 'cdn'
settings.resources = 'inline'

# Palette: https://coolors.co/palette/0466c8-0353a4-023e7d-002855-001845-001233-33415c-5c677d-7d8597-979dac
dark_color = '#292929'
light_color = '#F8F8F9'
footprint_colors = {'good': '#58D68D', 'best': '#9B59B6'}

colorbar_opts = {'background_fill_color': light_color}
grid_opts = {'grid_line_dash': [6, 4], 'grid_line_alpha': .5}
control_width = 280


@dataclass
class Content:
    name: str = ""
    main: Any = None
    control: Any = None


@dataclass
class Layout:
    space: Content = field(default_factory=Content)
    performance: Content = field(default_factory=Content)
    dists: Content = field(default_factory=Content)
    explorer: Content = field(default_factory=Content)


class ClassificationApp:
    """
    Classification app class.

    Args:
        workspace (Workspace): loaded workspace instance
    """
    _tabs_labels = ['Instance Space', 'Footprint Performance', 'Distributions', 'Data Explorer']

    def __init__(self, workspace: Workspace):
        pn.extension('plotly')
        hv.extension('bokeh')

        self.workspace = workspace
        self.bbox = None
        self.cmap = 'coolwarm'
        self.tabs = pn.Tabs(*[(name, None) for name in self._tabs_labels], dynamic=True)

        self.all_cols = (
                workspace.data.columns.to_list() +
                workspace.extended_metadata.columns.to_list() +
                workspace.is_coordinates.columns.to_list()
        )
        self.output_col = workspace.data.columns[-1]

        df_dataset = workspace.data.copy()
        df_metadata = workspace.extended_metadata
        df_is = workspace.is_coordinates
        df_footprint = workspace.footprints

        if len(df_dataset.columns) > 3:
            X = df_dataset.iloc[:, :-1]
            y = df_dataset.iloc[:, -1]

            pca = PCA(n_components=2)
            X_embedded = pca.fit_transform(X)

            df = pd.DataFrame(X_embedded, columns=['Component1', 'Component2'], index=X.index)
            df_dataset = pd.concat([df, y], axis=1)

        data = df_is.join(df_dataset)
        self.data = data.join(df_metadata)
        # self.ds = hv.Dataset(self.data.reset_index())
        # self.selection = link_selections.instance(
        #     unselected_alpha=0.2,
        #     # unselected_color='#CBCED5',
        #     show_regions=False
        # )

        self.data_dims = df_dataset.columns.to_list()
        self.class_label = self.data_dims[2]
        self.meta_dims = df_metadata.columns.to_list()

        # Scatter kdims and vdims
        is_cols = df_is.columns.to_list()
        self.is_kdims = is_cols[0]
        self.is_vdims = [is_cols[1], self.class_label] + self.meta_dims
        self.data_kdims = self.data_dims[0]
        self.data_vdims = [self.data_dims[1], self.class_label] + self.meta_dims

        # Markers
        markers = ['circle', 'triangle', 'square', 'diamond', 'asterisk', 'hex', '+', 'x']
        cat = np.sort(df_dataset[self.class_label].unique())
        if len(cat) > len(markers):
            self.marker = dim(self.class_label).categorize(dict(zip(cat, list(MarkerType))))
        else:
            self.marker = dim(self.class_label).categorize(dict(zip(cat, markers)))

        # Main tab widgets
        self.w_color = pn.widgets.Select(options=self.meta_dims + [self.class_label], value=self.meta_dims[0])
        self.w_color_range = pn.widgets.RangeSlider(start=0, end=20, value=(0, 5), step=0.5)
        self.w_checkbox = pn.widgets.Checkbox(name='manual colorbar range', value=False)
        self.w_footprint_on = pn.widgets.Checkbox(name='draw footprint area', value=True)

        # Distributions tab widgets
        cols = workspace.data.columns.to_list()
        cols.remove(self.output_col)
        self.feat_cols = cols
        self.meta_cols = df_metadata.columns.to_list()
        self.w_dist_source = pn.widgets.RadioBoxGroup(
            name='Source',
            options=['Features', 'Hardness Measures'],
            inline=False
        )
        self.w_dist_type = pn.widgets.Select(name='Plot type', options=['Histogram', 'Bar', 'Box'])
        self.w_dist_var = pn.widgets.Select(name='Feature', options=cols)
        self.w_box_vars = pn.widgets.MultiChoice(
            name='Boxplot variables', value=cols[:2],
            options=cols,
            disabled=True,
            solid=False
        )

        # Data explorer tab widgets
        self.w_var_y = pn.widgets.Select(name='y-axis', options=self.all_cols, value='z_2')
        self.w_var_x = pn.widgets.Select(name='x-axis', options=self.all_cols, value='z_1')
        self.w_var_c = pn.widgets.Select(name='Color', options=self.all_cols, value=self.output_col)
        self.w_var_cm = pn.widgets.RadioButtonGroup(
            name='Color map',
            options=['Continuous', 'Discrete'],
            button_type='default',
            value='Continuous'
        )
        self.w_var_s = pn.widgets.DiscreteSlider(name='Size', options=list(range(1, 16)), value=7)

        val = 'instance_easiness' if 'instance_easiness' in df_footprint.index else ''
        self.w_footprint_algo = pn.widgets.Select(options=df_footprint.index.unique(level='algo').to_list(), value=val)

        # Download
        self.w_group_data = pn.widgets.CheckButtonGroup(
            name='Data sources',
            options=['Features', 'Meta-features', 'IS coordinates'],
            value=['Features'],
            button_type='warning',
            max_width=control_width
        )

        # Layout
        self.layout = Layout()
        self.sidebar = pn.Column("")

    @staticmethod
    def footprint2polygons(footprint: np.ndarray) -> MultiPolygon:
        poly_list = np.split(footprint, np.argwhere(np.isnan(footprint).any(axis=1)).flatten())
        return MultiPolygon(list(map(lambda x: Polygon(x[~np.isnan(x).any(axis=1)]), poly_list)))

    def footprint_area(self, algo: str):
        """
        Draws footprint area of a given algorithm.

        Args:
            algo (str): algorithm name

        Returns:
            Polygon plot with good and bad footprints
        """
        try:
            border_points_good = self.workspace.footprints.xs((algo, 'good')).values
        except KeyError:
            border_points_good = np.array([[0, 0]])
        try:
            border_points_best = self.workspace.footprints.xs((algo, 'best')).values
        except KeyError:
            border_points_best = np.array([[0, 0]])

        border_good, border_best = border_points_good, border_points_best

        footprint_good = hv.Polygons(
            [border_good.tolist()],
            label='Good Footprint'
        ).opts(
            line_width=1, line_alpha=0.2,
            line_color='black',
            fill_color=footprint_colors['good'],
            fill_alpha=.2,
            show_legend=True
        )

        footprint_best = hv.Polygons(
            [border_best.tolist()],
            label='Best Footprint'
        ).opts(
            line_width=1,
            line_alpha=0.2,
            line_color='black',
            fill_color=footprint_colors['best'],
            fill_alpha=.2,
            show_legend=True
        )
        return footprint_good * footprint_best

    def select_instances(self) -> Union[pd.Series, pd.DataFrame]:
        """
        Returns a mask of the instances within the selection.
        """
        if self.bbox is None:
            return pd.Series(True, index=self.data.index)
        x, y = list(self.bbox.keys())
        if len(self.bbox[x]) == 2:
            V1 = np.column_stack([self.bbox[x], self.bbox[y]])
            V2 = V1.copy()
            V2[0, 1], V2[1, 1] = V1[1, 1], V1[0, 1]
            V = np.array([V1[0, :], V2[0, :], V1[1, :], V2[1, :]])
            contour = list(map(tuple, V))
        else:
            contour = list(map(tuple, np.column_stack([self.bbox[x], self.bbox[y]])))
        polygon = Polygon(contour)
        mask = self.data[[x, y]].apply(lambda p: polygon.contains(Point(p[0], p[1])), raw=True, axis=1)
        return mask

        # df = self.ds.select(selection_expr=self.selection.selection_expr).dframe()
        # df = df.set_index(self.workspace.INDEX)
        # return self.workspace.data.loc[df.index]

    def select_footprint_instances(self, ftype: str = 'good') -> list:
        """
        Returns a mask of the instances within the current footprint.

        Args:
            ftype: type of footprint ('good' or 'bad')

        Returns:
            list: instance mask

        """
        Z = self.workspace.is_coordinates.values
        algo = self.w_footprint_algo.value
        try:
            boundary = self.workspace.footprints.xs([algo, ftype]).values
        except KeyError:
            return [False] * Z.shape[0]
        poly = self.footprint2polygons(boundary)
        return [poly.contains(p) or poly.boundary.contains(p) for p in MultiPoint(Z)]

    def data_space(self, color: str, range_limits: Tuple[Number, Number], autorange_on: bool) -> hv.Scatter:
        """
        Creates the data space (PCA) plot.

        Args:
            color: name of the variable to color by
            range_limits: color bar ranges
            autorange_on: whether to use auto range for color bar

        Returns:
            Data space scatter plot

        """
        if not autorange_on:
            range_limits = (np.nan, np.nan)
        cmap = self.cmap
        hover_list = [
            (self.output_col, self.output_col),
            ('Component 1', 'Component1'),
            ('Component 2', 'Component2'),
            ('Instance Hardness', 'instance_hardness'),
            (' '.join(str.split(color, '_', 1)), color)
        ]
        hover_list = list(dict.fromkeys(hover_list))
        tooltips = [(s[0], '@' + s[1]) for s in hover_list]  # [("Instance", "$index")] +
        hover = HoverTool(tooltips=tooltips)
        scatter_pca = hv.Scatter(
            self.data,
            kdims=self.data_kdims,
            vdims=self.data_vdims
        ).opts(
            responsive=True,
            aspect=1.1,
            color=color,
            cmap=cmap,
            show_grid=True,
            gridstyle=grid_opts,
            marker=self.marker,
            tools=['lasso_select', 'box_select', hover],
            size=7,
            framewise=True,
            colorbar=True,
            colorbar_opts=colorbar_opts,
            clim=range_limits
        )
        return scatter_pca

    def instance_space(self, color: str, range_limits: Tuple[Number, Number], autorange_on: bool) -> hv.Scatter:
        """
        Creates the instance space plot.

        Args:
            color: name of the variable to color by
            range_limits: color bar ranges
            autorange_on: whether to use auto range for color bar

        Returns:
            Instance Space scatter plot

        """
        if not autorange_on:
            range_limits = (np.nan, np.nan)
        cmap = self.cmap
        hover_list = [
            (self.output_col, self.output_col),
            ('z1', 'z_1'),
            ('z2', 'z_2'),
            ('Instance Hardness', 'instance_hardness'),
            (' '.join(str.split(color, '_', 1)), color)
        ]
        hover_list = list(dict.fromkeys(hover_list))
        tooltips = [(s[0], '@' + s[1]) for s in hover_list]  # [("Instance", "$index")] +
        hover = HoverTool(tooltips=tooltips)
        scatter_is = hv.Scatter(
            self.data,
            kdims=self.is_kdims,
            vdims=self.is_vdims
        ).opts(
            responsive=True,
            aspect=1.1,
            color=color,
            cmap=cmap,
            show_grid=True,
            gridstyle=grid_opts,
            marker=self.marker,
            tools=['lasso_select', 'box_select', hover],
            size=7,
            framewise=True,
            colorbar=True,
            colorbar_opts=colorbar_opts,
            clim=range_limits
        )
        return scatter_is

    def get_download_data(self, mask: Union[pd.Series, List[bool]]) -> pd.DataFrame:
        sources = []
        if len(self.w_group_data.value) == 0:
            df = pd.DataFrame()
        else:
            for group in self.w_group_data.value:
                if group == 'Features':
                    sources.append(self.workspace.data[mask])
                elif group == 'Meta-features':
                    sources.append(self.workspace.extended_metadata[mask])
                elif group == 'IS coordinates':
                    sources.append(self.workspace.is_coordinates[mask])
            df = pd.concat(sources, axis=1)
        return df

    def render_projection_panel(self):
        """
        Builds and returns the entire panel, with tabs and plots.

        Returns:
            panel Template
        """

        @pn.depends(color=self.w_color.param.value, lim=self.w_color_range.param.value,
                    autorange_on=self.w_checkbox.param.value)
        def update_pca_plot(color, lim, autorange_on):
            return self.data_space(color, lim, autorange_on)

        @pn.depends(color=self.w_color.param.value, lim=self.w_color_range.param.value,
                    autorange_on=self.w_checkbox.param.value)
        def update_isa_plot(color, lim, autorange_on):
            return self.instance_space(color, lim, autorange_on)

        def selection_callback_pca(bbox, region_element, selection_expr, resetting):
            if resetting:
                bbox = None

            if self.bbox is not bbox:
                self.bbox = bbox

            return hv.Polygons([[[0, 0]]])

        @pn.depends(footprint=self.w_footprint_algo.param.value, fp_on=self.w_footprint_on.param.value)
        def selection_callback_isa(bbox, region_element, selection_expr, footprint, fp_on):
            if self.bbox is not bbox:
                self.bbox = bbox

            if fp_on:
                return self.footprint_area(footprint)
            else:
                return (hv.Polygons([[[0, 0]]], label='Good Footprint').opts(fill_color=footprint_colors['good']) *
                        hv.Polygons([[[0, 0]]], label='Best Footprint').opts(fill_color=footprint_colors['best']))

        dmap_pca = hv.DynamicMap(update_pca_plot)
        dmap_isa = hv.DynamicMap(update_isa_plot)
        dmap_pca.opts(title='Principal Components')
        dmap_isa.opts(title='Instance Space')

        selection_pca = SelectionExpr(source=dmap_pca)
        reset = PlotReset()
        sel1_dmap = hv.DynamicMap(selection_callback_pca, streams=[selection_pca, reset])

        selection_isa = SelectionExpr(source=dmap_isa)
        sel2_dmap = hv.DynamicMap(selection_callback_isa, streams=[selection_isa])

        def download_selection_points():
            mask = self.select_instances()
            df = self.get_download_data(mask)
            sio = io.StringIO()
            df.to_csv(sio)
            sio.seek(0)
            return sio

        button_download = pn.widgets.FileDownload(
            embed=False,
            auto=True,
            callback=download_selection_points,
            filename='selection.csv',
            label='Save selected points',
            button_type='default'
        )

        def download_footprint_points(ftype: str = 'good'):
            mask = self.select_footprint_instances(ftype)
            df = self.get_download_data(mask)
            sio = io.StringIO()
            df.to_csv(sio)
            sio.seek(0)
            return sio

        button_download_fp_good = pn.widgets.FileDownload(
            embed=False,
            auto=True,
            callback=lambda: download_footprint_points('good'),
            filename='good_footprint_instances.csv',
            label='Save good footprint points',
            button_type='default'
        )
        button_download_fp_best = pn.widgets.FileDownload(
            embed=False,
            auto=True,
            callback=lambda: download_footprint_points('best'),
            filename='best_footprint_instances.csv',
            label='Save best footprint points',
            button_type='default'
        )

        main = (dmap_pca * sel1_dmap + dmap_isa * sel2_dmap).cols(2).opts(
            opts.Layout(shared_axes=False, shared_datasource=True, framewise=True),
            opts.Scatter(bgcolor='#F8F8F9'),
            opts.Polygons(show_legend=True, legend_position='bottom_left'),
            opts.Overlay(legend_opts={"click_policy": "hide", }),
        )

        control = pn.Column(
            '## Color', self.w_color,
            '### Color Bar', self.w_checkbox, self.w_color_range,
            pn.Row(pn.Spacer(), height=20),
            '## Footprint', self.w_footprint_on, self.w_footprint_algo,
            pn.Row(pn.Spacer(), height=20),
            '## Selection \nChoose the data sources:', self.w_group_data, pn.Spacer(height=10),
            button_download, button_download_fp_good, button_download_fp_best,
            width=control_width
        )

        self.layout.space.name = self._tabs_labels[0]
        self.layout.space.main = main
        self.layout.space.control = control

    def render_performance_panel(self):
        table = pn.widgets.DataFrame(
            self.workspace.footprint_performance,
            name='Performance',
            disabled=True,
            sizing_mode='stretch_both'
        )
        self.layout.performance.name = self._tabs_labels[1]
        self.layout.performance.main = table
        self.layout.performance.control = ""

    def render_dist_panel(self):
        @pn.depends(g=self.w_dist_source, watch=True)
        def update_var_list(g):
            if g == 'Features':
                self.w_dist_var.options = self.feat_cols
            else:
                self.w_dist_var.options = self.meta_cols

        @pn.depends(
            a=self.tabs.param.active,
            dist_type=self.w_dist_type.param.value,
            var=self.w_dist_var.param.value,
            source=self.w_dist_source.param.value
        )
        def plot_dist(a, dist_type, var, source):
            if a != 2:
                return ""
            mask = self.select_instances()
            output_col = self.output_col

            if source == 'Features':
                df_full = self.workspace.data.copy()
            else:
                df_full = self.workspace.extended_metadata.copy()
                df_full = df_full.join(self.workspace.data[output_col])
            df_full.loc[:, output_col] = df_full[output_col].apply(lambda x: str(x))

            df_selection = df_full[mask].copy()
            df_selection.loc[:, output_col] = df_selection[output_col].apply(lambda x: str(x))
            classes = df_selection[output_col].unique().tolist()
            classes.sort()
            category_orders = {output_col: classes}
            fig = None

            if dist_type == 'Histogram':
                fig = px.histogram(
                    df_selection,
                    x=var,
                    color=output_col,
                    category_orders=category_orders
                )
            elif dist_type == 'Bar':
                df_count = df_selection[[var, output_col]].value_counts()
                df_count.name = 'count'
                df_count = df_count.to_frame().reset_index()
                fig = px.bar(
                    df_count,
                    x=var,
                    y="count",
                    color=output_col,
                    category_orders=category_orders
                )
            elif dist_type == 'Box':
                df_full['Group'] = 'All instances'
                df_selection['Group'] = 'Selected instances'
                fig = px.box(
                    pd.concat([df_selection, df_full]),
                    x='Group',
                    y=var,
                    color=output_col,
                    category_orders=category_orders
                )

            fig.update_layout(
                margin=dict(l=0, r=0, t=20, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                modebar={'bgcolor': 'rgba(255,255,255,0)'},
                font_family="'Source Sans Pro', verdana, arial",
                legend_font_size=14,
                font_size=16
            )
            fig.layout.autosize = True
            return pn.Column(
                pn.pane.Plotly(fig),
                sizing_mode="stretch_width"
            )

        self.layout.dists.name = self._tabs_labels[2]
        self.layout.dists.main = plot_dist
        self.layout.dists.control = pn.Column(
            self.w_dist_source,
            pn.Spacer(),
            self.w_dist_type,
            self.w_dist_var,
            width=control_width
        )

    def render_explorer_panel(self):
        @pn.depends(a=self.tabs.param.active, x=self.w_var_x, y=self.w_var_y, c=self.w_var_c.param.value)
        def plot_scatter(a, x, y, c):
            if a != 3:
                return ""
            mask = self.select_instances()
            output_col = self.output_col
            df_all = self.workspace.data[mask].copy()
            df_all = df_all.join(self.workspace.extended_metadata, how='left')
            df_all = df_all.join(self.workspace.is_coordinates, how='left')
            df_all.loc[:, output_col] = df_all[output_col].apply(lambda v: str(v))
            classes = df_all[output_col].unique().tolist()
            classes.sort()
            category_orders = {output_col: classes}

            fig_plotly = px.scatter(
                df_all,
                x=x,
                y=y,
                color=c,
                # marginal_x="histogram",
                # marginal_y="histogram",
                category_orders=category_orders
            )
            fig_plotly.update_layout(
                margin=dict(l=0, r=0, t=20, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                modebar={'bgcolor': 'rgba(255,255,255,0)'},
                font_family="'Source Sans Pro', verdana, arial",
                legend_font_size=15,
                font_size=16
            )
            fig_plotly.layout.autosize = True
            return pn.Column(
                pn.pane.Plotly(fig_plotly, aspect_ratio=2),
                sizing_mode="stretch_width"
            )

        self.layout.explorer.name = self._tabs_labels[3]
        self.layout.explorer.main = plot_scatter
        self.layout.explorer.control = pn.Column(self.w_var_x, self.w_var_y, self.w_var_c, width=control_width)

    def populate_tabs(self):
        """
        Populates the panel tabs.
        """
        self.tabs[0] = (self.layout.space.name, self.layout.space.main)
        self.tabs[1] = (self.layout.performance.name, self.layout.performance.main)
        self.tabs[2] = (self.layout.dists.name, self.layout.dists.main)
        self.tabs[3] = (self.layout.explorer.name, self.layout.explorer.main)

    def render_panel(self):
        control_list = [
            self.layout.space.control,
            self.layout.performance.control,
            self.layout.dists.control,
            self.layout.explorer.control
        ]
        self.sidebar[0] = control_list[0]

        @pn.depends(a=self.tabs.param.active, watch=True)
        def update_control(a):
            self.sidebar[0] = control_list[a]

        fast_list = pn.template.FastListTemplate(
            site="",
            title="PyHard",
            sidebar=[self.sidebar],
            main=[
                self.tabs,
            ],
            # modal=["", sizing_mode='stretch_width')],
            header_background="#0466C8",
            accent_base_color="#CBCED5",
            neutral_color='#7D8597',
            font='Source Sans Pro',
            font_url="https://fonts.googleapis.com/css2?family=Source+Sans+Pro",
            main_layout='',
            # sidebar_footer="Info",
            favicon=str(_my_path / "midia/blobs.svg"),
            background_color='#F8F8F9',
            sidebar_width=285,
            theme_toggle=False,
            meta_author='Pedro Paiva'
        )

        return fast_list

    def start(self, port: int = 5001, show: bool = True, ntries: int = 5):
        """
        Starts the application server.

        Args:
            port (int): attempts first to use this port. If it is in use, increments by 1 and try again until `ntries`
                is reached
            show: whether to open the browser and show the app
            ntries: maximum number of increments to try if `port` is in use
        """
        self.render_projection_panel()
        self.render_performance_panel()
        self.render_dist_panel()
        self.render_explorer_panel()
        self.populate_tabs()
        panel = self.render_panel()
        for _ in range(ntries):
            try:
                pn.serve(
                    panel,
                    port=port,
                    show=show,
                    title='Instance Hardness',
                    websocket_origin=[f'127.0.0.1:{port}', f'localhost:{port}']
                )
                break
            except OSError:
                print(f"Port {port} already in use. Retrying with next port...")
                port += 1


if __name__ == "__main__":
    ws = Workspace(_my_path / "data/wine/")
    ws.load()
    app = ClassificationApp(ws)
    app.start(show=True)
