"""
Implements support for matplotlib extensions such as pyplot.plot.
"""
import sys
import matplotlib
import matplotlib.pyplot as plt
import numba
import numpy as np
from numba.core import ir_utils, types
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, bound_function, infer_global, signature
from numba.extending import NativeValue, box, infer_getattr, models, overload, overload_method, register_model, typeof_impl, unbox
import bodo
from bodo.utils.typing import BodoError, gen_objmode_func_overload, gen_objmode_method_overload, get_overload_const_int, is_overload_constant_bool, is_overload_constant_int, is_overload_true, raise_bodo_error
from bodo.utils.utils import unliteral_all
mpl_plt_kwargs_funcs = ['gca', 'plot', 'scatter', 'bar', 'contour',
    'contourf', 'quiver', 'pie', 'fill', 'fill_between', 'step', 'text',
    'errorbar', 'barbs', 'eventplot', 'hexbin', 'xcorr', 'imshow',
    'subplots', 'suptitle', 'tight_layout']
mpl_axes_kwargs_funcs = ['annotate', 'plot', 'scatter', 'bar', 'contour',
    'contourf', 'quiver', 'pie', 'fill', 'fill_between', 'step', 'text',
    'errorbar', 'barbs', 'eventplot', 'hexbin', 'xcorr', 'imshow',
    'set_xlabel', 'set_ylabel', 'set_xscale', 'set_yscale',
    'set_xticklabels', 'set_yticklabels', 'set_title', 'legend', 'grid',
    'tick_params', 'get_figure', 'set_xticks', 'set_yticks']
mpl_figure_kwargs_funcs = ['suptitle', 'tight_layout', 'set_figheight',
    'set_figwidth']
mpl_gather_plots = ['plot', 'scatter', 'bar', 'contour', 'contourf',
    'quiver', 'pie', 'fill', 'fill_between', 'step', 'errorbar', 'barbs',
    'eventplot', 'hexbin', 'xcorr', 'imshow']


def install_mpl_class(types_name, python_type):
    beflm__ephe = ''.join(map(str.title, types_name.split('_')))
    slnax__tgou = f'class {beflm__ephe}(types.Opaque):\n'
    slnax__tgou += '    def __init__(self):\n'
    slnax__tgou += (
        f"       types.Opaque.__init__(self, name='{beflm__ephe}')\n")
    slnax__tgou += '    def __reduce__(self):\n'
    slnax__tgou += (
        f"        return (types.Opaque, ('{beflm__ephe}',), self.__dict__)\n")
    oafdg__utr = {}
    exec(slnax__tgou, {'types': types, 'bodo': bodo}, oafdg__utr)
    zwq__avke = oafdg__utr[beflm__ephe]
    aahsu__shvx = sys.modules[__name__]
    setattr(aahsu__shvx, beflm__ephe, zwq__avke)
    class_instance = zwq__avke()
    setattr(types, types_name, class_instance)
    register_model(zwq__avke)(models.OpaqueModel)
    typeof_impl.register(python_type)(lambda val, c: class_instance)
    unbox(zwq__avke)(unbox_mpl_obj)
    box(zwq__avke)(box_mpl_obj)


def unbox_mpl_obj(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


def box_mpl_obj(typ, val, c):
    c.pyapi.incref(val)
    return val


def _install_mpl_types():
    trv__msg = [('mpl_figure_type', matplotlib.figure.Figure), (
        'mpl_axes_type', matplotlib.axes.Axes), ('mpl_text_type',
        matplotlib.text.Text), ('mpl_annotation_type', matplotlib.text.
        Annotation), ('mpl_line_2d_type', matplotlib.lines.Line2D), (
        'mpl_path_collection_type', matplotlib.collections.PathCollection),
        ('mpl_bar_container_type', matplotlib.container.BarContainer), (
        'mpl_quad_contour_set_type', matplotlib.contour.QuadContourSet), (
        'mpl_quiver_type', matplotlib.quiver.Quiver), ('mpl_wedge_type',
        matplotlib.patches.Wedge), ('mpl_polygon_type', matplotlib.patches.
        Polygon), ('mpl_poly_collection_type', matplotlib.collections.
        PolyCollection), ('mpl_axes_image_type', matplotlib.image.AxesImage
        ), ('mpl_errorbar_container_type', matplotlib.container.
        ErrorbarContainer), ('mpl_barbs_type', matplotlib.quiver.Barbs), (
        'mpl_event_collection_type', matplotlib.collections.EventCollection
        ), ('mpl_line_collection_type', matplotlib.collections.LineCollection)]
    for pbpz__khh, jnci__kzm in trv__msg:
        install_mpl_class(pbpz__khh, jnci__kzm)


_install_mpl_types()


def generate_matplotlib_signature(return_typ, args, kws, obj_typ=None):
    kws = dict(kws)
    asrt__qczkf = ', '.join(f'e{fqt__qao}' for fqt__qao in range(len(args)))
    if asrt__qczkf:
        asrt__qczkf += ', '
    wuzfq__ydldx = ', '.join(f"{wskl__xyur} = ''" for wskl__xyur in kws.keys())
    dlx__hhbyb = 'matplotlib_obj, ' if obj_typ is not None else ''
    shsh__knsx = f'def mpl_stub({dlx__hhbyb} {asrt__qczkf} {wuzfq__ydldx}):\n'
    shsh__knsx += '    pass\n'
    dck__utf = {}
    exec(shsh__knsx, {}, dck__utf)
    bvmsg__drntw = dck__utf['mpl_stub']
    hqu__ynj = numba.core.utils.pysignature(bvmsg__drntw)
    ocyo__uihmb = ((obj_typ,) if obj_typ is not None else ()) + args + tuple(
        kws.values())
    return signature(return_typ, *unliteral_all(ocyo__uihmb)).replace(pysig
        =hqu__ynj)


def generate_axes_typing(mod_name, nrows, ncols):
    oxxxp__qaj = '{}.subplots(): {} must be a constant integer >= 1'
    if not is_overload_constant_int(nrows):
        raise_bodo_error(oxxxp__qaj.format(mod_name, 'nrows'))
    if not is_overload_constant_int(ncols):
        raise_bodo_error(oxxxp__qaj.format(mod_name, 'ncols'))
    ocbo__jcf = get_overload_const_int(nrows)
    cmvmz__dxgq = get_overload_const_int(ncols)
    if ocbo__jcf < 1:
        raise BodoError(oxxxp__qaj.format(mod_name, 'nrows'))
    if cmvmz__dxgq < 1:
        raise BodoError(oxxxp__qaj.format(mod_name, 'ncols'))
    if ocbo__jcf == 1 and cmvmz__dxgq == 1:
        daga__puk = types.mpl_axes_type
    else:
        if cmvmz__dxgq == 1:
            kqr__erbq = types.mpl_axes_type
        else:
            kqr__erbq = types.Tuple([types.mpl_axes_type] * cmvmz__dxgq)
        daga__puk = types.Tuple([kqr__erbq] * ocbo__jcf)
    return daga__puk


def generate_pie_return_type(args, kws):
    sskt__cgdin = args[4] if len(args) > 5 else kws.get('autopct', types.none)
    if sskt__cgdin == types.none:
        return types.Tuple([types.List(types.mpl_wedge_type), types.List(
            types.mpl_text_type)])
    return types.Tuple([types.List(types.mpl_wedge_type), types.List(types.
        mpl_text_type), types.List(types.mpl_text_type)])


def generate_xcorr_return_type(func_mod, args, kws):
    plo__kyc = args[4] if len(args) > 5 else kws.get('usevlines', True)
    if not is_overload_constant_bool(plo__kyc):
        raise_bodo_error(
            f'{func_mod}.xcorr(): usevlines must be a constant boolean')
    if is_overload_true(plo__kyc):
        return types.Tuple([types.Array(types.int64, 1, 'C'), types.Array(
            types.float64, 1, 'C'), types.mpl_line_collection_type, types.
            mpl_line_2d_type])
    return types.Tuple([types.Array(types.int64, 1, 'C'), types.Array(types
        .float64, 1, 'C'), types.mpl_line_2d_type, types.none])


@infer_global(plt.plot)
class PlotTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.List(types.
            mpl_line_2d_type), args, kws)


@infer_global(plt.step)
class StepTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.List(types.
            mpl_line_2d_type), args, kws)


@infer_global(plt.scatter)
class ScatterTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.mpl_path_collection_type,
            args, kws)


@infer_global(plt.bar)
class BarTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.mpl_bar_container_type,
            args, kws)


@infer_global(plt.contour)
class ContourTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.
            mpl_quad_contour_set_type, args, kws)


@infer_global(plt.contourf)
class ContourfTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.
            mpl_quad_contour_set_type, args, kws)


@infer_global(plt.quiver)
class QuiverTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.mpl_quiver_type, args, kws)


@infer_global(plt.fill)
class FillTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.List(types.
            mpl_polygon_type), args, kws)


@infer_global(plt.fill_between)
class FillBetweenTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.mpl_poly_collection_type,
            args, kws)


@infer_global(plt.pie)
class PieTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(generate_pie_return_type(args,
            kws), args, kws)


@infer_global(plt.text)
class TextTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.mpl_text_type, args, kws)


@infer_global(plt.errorbar)
class ErrorbarTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.
            mpl_errorbar_container_type, args, kws)


@infer_global(plt.barbs)
class BarbsTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.mpl_barbs_type, args, kws)


@infer_global(plt.eventplot)
class EventplotTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.List(types.
            mpl_event_collection_type), args, kws)


@infer_global(plt.hexbin)
class HexbinTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.mpl_poly_collection_type,
            args, kws)


@infer_global(plt.xcorr)
class XcorrTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(generate_xcorr_return_type(
            'matplotlib.pyplot', args, kws), args, kws)


@infer_global(plt.imshow)
class ImshowTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.mpl_axes_image_type,
            args, kws)


@infer_global(plt.gca)
class GCATyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.mpl_axes_type, args, kws)


@infer_global(plt.suptitle)
class SuptitleTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.mpl_text_type, args, kws)


@infer_global(plt.tight_layout)
class TightLayoutTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.none, args, kws)


@infer_global(plt.subplots)
class SubplotsTyper(AbstractTemplate):

    def generic(self, args, kws):
        nrows = args[0] if len(args) > 0 else kws.get('nrows', types.literal(1)
            )
        ncols = args[1] if len(args) > 1 else kws.get('ncols', types.literal(1)
            )
        otnxb__ned = generate_axes_typing('matplotlib.pyplot', nrows, ncols)
        return generate_matplotlib_signature(types.Tuple([types.
            mpl_figure_type, otnxb__ned]), args, kws)


SubplotsTyper._no_unliteral = True


@infer_getattr
class MatplotlibFigureKwargsAttribute(AttributeTemplate):
    key = MplFigureType

    @bound_function('fig.suptitle', no_unliteral=True)
    def resolve_suptitle(self, fig_typ, args, kws):
        return generate_matplotlib_signature(types.mpl_text_type, args, kws,
            obj_typ=fig_typ)

    @bound_function('fig.tight_layout', no_unliteral=True)
    def resolve_tight_layout(self, fig_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =fig_typ)

    @bound_function('fig.set_figheight', no_unliteral=True)
    def resolve_set_figheight(self, fig_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =fig_typ)

    @bound_function('fig.set_figwidth', no_unliteral=True)
    def resolve_set_figwidth(self, fig_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =fig_typ)


@infer_getattr
class MatplotlibAxesKwargsAttribute(AttributeTemplate):
    key = MplAxesType

    @bound_function('ax.annotate', no_unliteral=True)
    def resolve_annotate(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)

    @bound_function('ax.grid', no_unliteral=True)
    def resolve_grid(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)

    @bound_function('ax.plot', no_unliteral=True)
    def resolve_plot(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.List(types.
            mpl_line_2d_type), args, kws, obj_typ=ax_typ)

    @bound_function('ax.step', no_unliteral=True)
    def resolve_step(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.List(types.
            mpl_line_2d_type), args, kws, obj_typ=ax_typ)

    @bound_function('ax.scatter', no_unliteral=True)
    def resolve_scatter(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.mpl_path_collection_type,
            args, kws, obj_typ=ax_typ)

    @bound_function('ax.contour', no_unliteral=True)
    def resolve_contour(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.
            mpl_quad_contour_set_type, args, kws, obj_typ=ax_typ)

    @bound_function('ax.contourf', no_unliteral=True)
    def resolve_contourf(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.
            mpl_quad_contour_set_type, args, kws, obj_typ=ax_typ)

    @bound_function('ax.quiver', no_unliteral=True)
    def resolve_quiver(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.mpl_quiver_type, args,
            kws, obj_typ=ax_typ)

    @bound_function('ax.bar', no_unliteral=True)
    def resolve_bar(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.mpl_bar_container_type,
            args, kws, obj_typ=ax_typ)

    @bound_function('ax.fill', no_unliteral=True)
    def resolve_fill(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.List(types.
            mpl_polygon_type), args, kws, obj_typ=ax_typ)

    @bound_function('ax.fill_between', no_unliteral=True)
    def resolve_fill_between(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.mpl_poly_collection_type,
            args, kws, obj_typ=ax_typ)

    @bound_function('ax.pie', no_unliteral=True)
    def resolve_pie(self, ax_typ, args, kws):
        return generate_matplotlib_signature(generate_pie_return_type(args,
            kws), args, kws, obj_typ=ax_typ)

    @bound_function('ax.text', no_unliteral=True)
    def resolve_text(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.mpl_text_type, args, kws,
            obj_typ=ax_typ)

    @bound_function('ax.errorbar', no_unliteral=True)
    def resolve_errorbar(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.
            mpl_errorbar_container_type, args, kws, obj_typ=ax_typ)

    @bound_function('ax.barbs', no_unliteral=True)
    def resolve_barbs(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.mpl_barbs_type, args,
            kws, obj_typ=ax_typ)

    @bound_function('ax.eventplot', no_unliteral=True)
    def resolve_eventplot(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.List(types.
            mpl_event_collection_type), args, kws, obj_typ=ax_typ)

    @bound_function('ax.hexbin', no_unliteral=True)
    def resolve_hexbin(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.mpl_poly_collection_type,
            args, kws, obj_typ=ax_typ)

    @bound_function('ax.xcorr', no_unliteral=True)
    def resolve_xcorr(self, ax_typ, args, kws):
        return generate_matplotlib_signature(generate_xcorr_return_type(
            'matplotlib.axes.Axes', args, kws), args, kws, obj_typ=ax_typ)

    @bound_function('ax.imshow', no_unliteral=True)
    def resolve_imshow(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.mpl_axes_image_type,
            args, kws, obj_typ=ax_typ)

    @bound_function('ax.tick_params', no_unliteral=True)
    def resolve_tick_params(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)

    @bound_function('ax.set_xlabel', no_unliteral=True)
    def resolve_set_xlabel(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)

    @bound_function('ax.set_xticklabels', no_unliteral=True)
    def resolve_set_xticklabels(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.List(types.mpl_text_type
            ), args, kws, obj_typ=ax_typ)

    @bound_function('ax.set_yticklabels', no_unliteral=True)
    def resolve_set_yticklabels(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.List(types.mpl_text_type
            ), args, kws, obj_typ=ax_typ)

    @bound_function('ax.set_ylabel', no_unliteral=True)
    def resolve_set_ylabel(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)

    @bound_function('ax.set_xscale', no_unliteral=True)
    def resolve_set_xscale(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)

    @bound_function('ax.set_yscale', no_unliteral=True)
    def resolve_set_yscale(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)

    @bound_function('ax.set_title', no_unliteral=True)
    def resolve_set_title(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)

    @bound_function('ax.legend', no_unliteral=True)
    def resolve_legend(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)

    @bound_function('ax.get_figure', no_unliteral=True)
    def resolve_get_figure(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.mpl_figure_type, args,
            kws, obj_typ=ax_typ)

    @bound_function('ax.set_xticks', no_unliteral=True)
    def resolve_set_xticks(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)

    @bound_function('ax.set_yticks', no_unliteral=True)
    def resolve_set_yticks(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)


@overload(plt.savefig, no_unliteral=True)
def overload_savefig(fname, dpi=None, facecolor='w', edgecolor='w',
    orientation='portrait', format=None, transparent=False, bbox_inches=
    None, pad_inches=0.1, metadata=None):

    def impl(fname, dpi=None, facecolor='w', edgecolor='w', orientation=
        'portrait', format=None, transparent=False, bbox_inches=None,
        pad_inches=0.1, metadata=None):
        with bodo.objmode():
            plt.savefig(fname=fname, dpi=dpi, facecolor=facecolor,
                edgecolor=edgecolor, orientation=orientation, format=format,
                transparent=transparent, bbox_inches=bbox_inches,
                pad_inches=pad_inches, metadata=metadata)
    return impl


@overload_method(MplFigureType, 'subplots', no_unliteral=True)
def overload_subplots(fig, nrows=1, ncols=1, sharex=False, sharey=False,
    squeeze=True, subplot_kw=None, gridspec_kw=None):
    otnxb__ned = generate_axes_typing('matplotlib.figure.Figure', nrows, ncols)
    pbpz__khh = str(otnxb__ned)
    if not hasattr(types, pbpz__khh):
        pbpz__khh = f'objmode_type{ir_utils.next_label()}'
        setattr(types, pbpz__khh, otnxb__ned)
    shsh__knsx = f"""def impl(
        fig,
        nrows=1,
        ncols=1,
        sharex=False,
        sharey=False,
        squeeze=True,
        subplot_kw=None,
        gridspec_kw=None,
    ):
        with numba.objmode(axes="{pbpz__khh}"):
            axes = fig.subplots(
                nrows=nrows,
                ncols=ncols,
                sharex=sharex,
                sharey=sharey,
                squeeze=squeeze,
                subplot_kw=subplot_kw,
                gridspec_kw=gridspec_kw,
            )
            if isinstance(axes, np.ndarray):
                axes = tuple([tuple(elem) if isinstance(elem, np.ndarray) else elem for elem in axes])
        return axes
    """
    dck__utf = {}
    exec(shsh__knsx, {'numba': numba, 'np': np}, dck__utf)
    impl = dck__utf['impl']
    return impl


gen_objmode_func_overload(plt.show, output_type=types.none, single_rank=True)
gen_objmode_func_overload(plt.draw, output_type=types.none, single_rank=True)
gen_objmode_func_overload(plt.gcf, output_type=types.mpl_figure_type)
gen_objmode_method_overload(MplFigureType, 'show', matplotlib.figure.Figure
    .show, output_type=types.none, single_rank=True)
gen_objmode_method_overload(MplAxesType, 'set_xlim', matplotlib.axes.Axes.
    set_xlim, output_type=types.UniTuple(types.float64, 2))
gen_objmode_method_overload(MplAxesType, 'set_ylim', matplotlib.axes.Axes.
    set_ylim, output_type=types.UniTuple(types.float64, 2))
gen_objmode_method_overload(MplAxesType, 'draw', matplotlib.axes.Axes.draw,
    output_type=types.none, single_rank=True)
gen_objmode_method_overload(MplAxesType, 'set_axis_on', matplotlib.axes.
    Axes.set_axis_on, output_type=types.none)
gen_objmode_method_overload(MplAxesType, 'set_axis_off', matplotlib.axes.
    Axes.set_axis_off, output_type=types.none)
