import os
import click

@click.command(name='build_xml_ws')
@click.option('-i', '--filename', required=True, 
              help='Input xml file.')
@click.option('--binned/--unbinned', 'use_binned', default=False, show_default=True,
              help='Fit to binned data.')
@click.option('--data_storage_type', default="vector", show_default=True, 
              type=click.Choice(['vector', 'tree', 'composite']),
              help='Set RooAbsData StorageType. Available choices: "vector", "tree", "composite".')
@click.option('-d', '--basedir', default=None, 
              help='Base directory to which files in the xmls are referenced. '
                   'By default, the directory of the input xml file is used.')
@click.option('-t', '--minimizer_type', default="Minuit2", show_default=True,
              help='Minimizer type')
@click.option('-a', '--minimizer_algo', default="Migrad", show_default=True,
              help='Minimizer algorithm')
@click.option('-c', '--num_cpu', type=int, default=1, show_default=True,
              help='Number of CPUs to use per parameter')
@click.option('-e', '--eps', type=float, default=1.0, show_default=True,
              help='Convergence criterium')
@click.option('--retry', type=int, default=0, show_default=True,
              help='Maximum number of retries upon a failed fit')
@click.option('--strategy', type=int, default=1, show_default=True,
              help='Default minimization strategy')
@click.option('--print_level', type=int, default=-1, show_default=True,
              help='Minimizer print level')
@click.option('--fix-cache/--no-fix-cache', default=True, show_default=True,
              help='Fix StarMomentMorph cache')
@click.option('--fix-multi/--no-fix-cache',  default=True, show_default=True,
              help='Fix MultiPdf level 2')
@click.option('--max_calls', type=int, default=-1, show_default=True,
              help='Maximum number of function calls')
@click.option('--max_iters', type=int, default=-1, show_default=True,
              help='Maximum number of Minuit iterations')
@click.option('--optimize', type=int, default=2, show_default=True,
              help='Optimize constant terms')
@click.option('--offset/--no-offset', default=True, show_default=True,
              help='Offset likelihood')
@click.option('-v', '--verbosity',  default="INFO", show_default=True,
              help='verbosity level ("DEBUG", "INFO", "WARNING", "ERROR")')
def build_xml_ws(**kwargs):
    """
    Build workspace from XML config files
    """
    _kwargs = {}
    for arg_name in ["filename", "use_binned", "data_storage_type",
                     "basedir", "verbosity"]:
        _kwargs[arg_name] = kwargs.pop(arg_name)
    _kwargs['minimizer_config'] = kwargs
    from quickstats.components.workspaces import XMLWSBuilder
    builder = XMLWSBuilder(**_kwargs)
    builder.generate_workspace()
    
@click.command(name='modify_ws')
@click.option('-i', '--filename', 'source', required=True, 
              help='Input xml/json file.')
@click.option('-t', '--minimizer_type', default="Minuit2", show_default=True,
              help='Minimizer type')
@click.option('-a', '--minimizer_algo', default="Migrad", show_default=True,
              help='Minimizer algorithm')
@click.option('-c', '--num_cpu', type=int, default=1, show_default=True,
              help='Number of CPUs to use per parameter')
@click.option('-e', '--eps', type=float, default=1.0, show_default=True,
              help='Convergence criterium')
@click.option('--retry', type=int, default=0, show_default=True,
              help='Maximum number of retries upon a failed fit')
@click.option('--strategy', type=int, default=1, show_default=True,
              help='Default minimization strategy')
@click.option('--print_level', type=int, default=-1, show_default=True,
              help='Minimizer print level')
@click.option('--fix-cache/--no-fix-cache', default=True, show_default=True,
              help='Fix StarMomentMorph cache')
@click.option('--fix-multi/--no-fix-cache',  default=True, show_default=True,
              help='Fix MultiPdf level 2')
@click.option('--max_calls', type=int, default=-1, show_default=True,
              help='Maximum number of function calls')
@click.option('--max_iters', type=int, default=-1, show_default=True,
              help='Maximum number of Minuit iterations')
@click.option('--optimize', type=int, default=2, show_default=True,
              help='Optimize constant terms')
@click.option('--offset/--no-offset', default=True, show_default=True,
              help='Offset likelihood')
@click.option('-v', '--verbosity',  default="INFO", show_default=True,
              help='verbosity level ("DEBUG", "INFO", "WARNING", "ERROR")')
def modify_ws(**kwargs):
    """
    Modify workspace from XML/json config files
    """
    _kwargs = {}
    for arg_name in ["source", "verbosity"]:
        _kwargs[arg_name] = kwargs.pop(arg_name)
    _kwargs['minimizer_config'] = kwargs
    from quickstats.components.workspaces import XMLWSModifier
    modifier = XMLWSModifier(**_kwargs)
    modifier.create_modified_workspace()