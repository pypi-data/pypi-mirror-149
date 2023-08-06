import plotly.graph_objects as go
import numpy as np


class Scatter3D(object):
    def __init__(self,
                 x,
                 y,
                 z,
                 ):
        """
        :param x: np.ndarray or list
        :param y: np.ndarray or list
        :param z: np.ndarray or list

        Create a custom 3D scatter plot with plotly
        """
        self.x = x
        self.y = y
        self.z = z

    def plot(self,
             color=None,
             title: str = '',
             xlabel: str = '',
             ylabel: str = '',
             legend_title: str = '',
             size: tuple = (800, 600),
             marker_size: int = 5,
             x_range=None,
             y_range=None,
             z_range=None,
             n_ticks: int = 10,
             margin=None,
             line_width: float = .0,
             line_color: str = 'black',
             alpha: float = 0.8,
             show: bool = False,
             cmin: float = 0.,
             cmax: float = 1.,
             colorscale: str = 'Turbo'):

        """
        :param line_color: line color
        :param line_width: line width
        :param colorscale: color scale
        :param cmax: maximum value of the colorbar
        :param cmin: minimum value of the colorbar
        :param alpha: alpha
        :param margin: scene margins
        :param n_ticks: number of ticks on every axis
        :param x_range: x range
        :param z_range: z range
        :param y_range: y range
        :param marker_size: marker size
        :param color: nodal values for the color scale
        :param title: figure title
        :param xlabel: xlabel
        :param ylabel: ylabel
        :param legend_title: legend_title
        :param size: size of the figure
        :param show: show (or not) the figure
        :return fig: figure instance

        Create the 3d scatter plot
        """
        # color = color.reshape(-1, 1) if color is not None else color
        if margin is None:
            margin = dict(r=10, l=10, b=10, t=10)
        if z_range is None:
            z_range = [-1, 1]
        if y_range is None:
            y_range = [-1, 1]
        if x_range is None:
            x_range = [-1, 1]

        if isinstance(self.x, list) and isinstance(self.y, list) and isinstance(self.z, list):
            data = [go.Scatter3d(x=self.x[i], y=self.y[i], z=self.z[i],
                                 mode='markers',
                                 marker=dict(size=marker_size,
                                             color=color[i],
                                             colorscale=colorscale,
                                             opacity=alpha,
                                             colorbar=dict(thickness=20),
                                             cmin=cmin,
                                             cmax=cmax,
                                             line=dict(width=line_width,
                                                       color=line_color)
                                             )) for i in range(len(self.x))]
        else:
            data = [go.Scatter3d(x=self.x, y=self.y, z=self.z,
                                 mode='markers',
                                 marker=dict(size=marker_size,
                                             color=color,
                                             colorscale=colorscale,
                                             opacity=alpha,
                                             colorbar=dict(thickness=20),
                                             cmin=cmin,
                                             cmax=cmax,
                                             line=dict(width=line_width,
                                                       color=line_color)
                                             ))]

        fig = go.Figure(data=data,
                        layout=go.Layout(
                            width=size[0],
                            height=size[1],
                        ))

        fig.update_layout(
            title=title,
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            legend_title=legend_title,
            scene=dict(
                xaxis=dict(nticks=n_ticks, range=x_range, ),
                yaxis=dict(nticks=n_ticks, range=y_range, ),
                zaxis=dict(nticks=n_ticks, range=z_range, ), ),

            margin=margin
        )

        fig.show() if show else None
        return fig


def mesh_3d(
        x, y, z, i, j, k,
        color: np.ndarray = None,
        title: str = '',
        xlabel: str = '',
        ylabel: str = '',
        legend_title: str = '',
        size: tuple = (800, 600),
        x_range=None,
        y_range=None,
        z_range=None,
        n_ticks: int = 10,
        margin=None,
        show: bool = False,
        cmin: float = 0.,
        cmax: float = 1.,
        colorscale: str = 'Turbo',
        flatshading: bool = True,
        showscale: bool = False,
        paper_bgcolor: str = 'rgb(1,1,1)',
        title_x: float = .5,
        font_color: str = 'white',
        show_axis: bool = False
):
    if margin is None:
        margin = dict(r=10, l=10, b=10, t=50)
    if z_range is None:
        z_range = [-10, 10]
    if y_range is None:
        y_range = [-10, 10]
    if x_range is None:
        x_range = [-10, 10]

    mesh3d = go.Mesh3d(
        x=x,
        y=y,
        z=z,
        i=i,
        j=j,
        k=k,
        flatshading=flatshading,
        colorscale=colorscale,
        intensity=color,
        name=title,
        showscale=showscale,
        cmax=cmax,
        cmin=cmin,
    )

    layout = go.Layout(
        paper_bgcolor=paper_bgcolor,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        legend_title=legend_title,
        title_x=title_x,
        title_text=title,
        font_color=font_color,
        width=size[0],
        height=size[1],
        # scene_camera=dict(eye=dict(x=1.25, y=-1.25, z=1)),
        scene_xaxis_visible=show_axis,
        scene_yaxis_visible=show_axis,
        scene_zaxis_visible=show_axis,
        scene=dict(
            xaxis=dict(nticks=n_ticks, range=x_range, ),
            yaxis=dict(nticks=n_ticks, range=y_range, ),
            zaxis=dict(nticks=n_ticks, range=z_range, ), ),
        margin=margin
    )

    fig = go.Figure(data=[mesh3d], layout=layout)
    fig.show() if show else None
    return fig
