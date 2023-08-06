# PIpeline RUnner -- (c)2022 David SPORN
# GPL3
########################################
import copy
import logging

# library logger
LOGGER = logging.getLogger('pipeline_runner')

pipeline_exec = None
pipeline_jobs = []
pipeline_before_all = []
pipeline_before_each = []
pipeline_after_each = []
pipeline_after_all = []

def register_func(registry:list, func, stage:str=''):
    item = {
        'func':func,
        'stage':stage
    }
    LOGGER.debug(item)
    registry.append(item)
#
# Concepts :
# * pipeline stages
#
# class annotation
def pipeline(_func=None, *, stages: tuple):
    """
    The annotated function is the entry point to run the pipeline, and should
    return a dictionnary with environment objects to be used throughout the pipeline.

    It MUST be unique in the python application, in other words, the application is the pipeline.

    The pipeline is defined by a sequence of 'stages', a stage is just a name to be targeted by jobs and job hooks.
    """
    LOGGER.debug(f"Register pipeline stages : {stages}")
    # TODO registers the sequence of stages
    def decorator_pipeline(func):
        def wrapper_pipeline(*args, **kwargs):
            LOGGER.info(f"===[ START OF PIPELINE {func.__name__} ]===")
            result = func(*args, **kwargs)
            for befa in pipeline_before_all:
                befa['func'](env=result)
            for stage in stages:
                LOGGER.info(f"======[ START OF STAGE {stage} ]======")
                jobs = [j for j in pipeline_jobs if j['stage'] == stage or j['stage'] == '']
                before_each = [j for j in pipeline_before_each if j['stage'] == stage or j['stage'] == '']
                after_each = [j for j in pipeline_after_each if j['stage'] == stage or j['stage'] == '']
                for job in jobs:
                    env = copy.deepcopy(result)
                    for befe in before_each:
                        befe['func'](env=env)
                    job['func'](env=env)
                    for afte in after_each:
                        afte['func'](env=env)
                LOGGER.info(f"======[ END OF STAGE {stage} ]======")
            for afta in pipeline_after_all:
                afta['func'](env=env)
            LOGGER.info(f"===[ END OF PIPELINE {func.__name__} ]===")
            return result
        return wrapper_pipeline
    global pipeline_exec
    if _func is None:
        result = decorator_pipeline
        pipeline_exec = result
        return result
    else:
        result = decorator_pipeline(_func)
        pipeline_exec = result
        return result

def job(_func=None, **kwargs):
    """
    An actual job for the pipeline.

    A job can be attached to a specific stage, otherwise it is performed at each stage.
    """
    LOGGER.debug("Register job")
    def decorator(func):
        def wrapper(*args,**kwargs):
            return func(*args,**kwargs)
        stage = kwargs['stage'] if 'stage' in kwargs else ''
        register_func(pipeline_jobs, wrapper, stage)
        return wrapper
    if _func is None:
        return decorator
    else:
        return decorator(_func)

def before_all(func):
    """
    The annotated function is called before any job of the pipeline is performed.

    It is intended for setting up environment object that will be shared by all the jobs, e.g. a connection to a database.
    """
    LOGGER.debug(f"Register before_all")
    def wrapper_before_all(* args, **kwargs):
        # before
        # func(kwargs)
        # after
        pass
    result = func
    register_func(pipeline_before_all, result)
    return result

def after_all(func):
    """
    The annotated function is called after all jobs of the pipeline have been performed.

    It is intended for tearing down environment object shared by all the jobs, e.g. a connection to a database.
    """
    LOGGER.debug(f"Register after_all")
    def wrapper_after_all(* args, **kwargs):
        # before
        # func(kwargs)
        # after
        pass
    result = func
    register_func(pipeline_after_all, result)
    return result


def before_each(_func=None, *args, **kwargs):
    """
    The annotated function is called before each job of the specified stage, or any jobs when no stage is specified.
    """
    LOGGER.debug("Register before_each")
    def decorator(func):
        def wrapper(*args,**kwargs):
            return func(*args,**kwargs)
        stage = kwargs['stage'] if 'stage' in kwargs else ''
        register_func(pipeline_before_each, wrapper, stage)
        return wrapper
    if _func is None:
        return decorator
    else:
        return decorator(_func)

def after_each(_func=None, **kwargs):
    """
    The annotated function is called after each job of the specified stage, or any jobs when no stage is specified.
    """
    LOGGER.debug("Register after_each")
    def decorator(func):
        def wrapper(*args,**kwargs):
            return func(*args,**kwargs)
        stage = kwargs['stage'] if 'stage' in kwargs else ''
        register_func(pipeline_after_each, wrapper, stage)
        return wrapper
    if _func is None:
        return decorator
    else:
        return decorator(_func)
