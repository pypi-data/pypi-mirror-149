"""
PIRUPY : A PIpeline RUnner for PYthon
=====================================

A set of annotations to define a set of 'jobs' regrouped into a sequence of 'stages', forming a 'pipeline'. Pipelines
and jobs have hooks to perform pre-processings and post-processings.

The principle for ordering calls is to follows the order of appearance. As such, inside a stage, the jobs will be called
following the same order than how they appear in the application. Same for the order of calling 'before all' hooks,
'before each' hooks, 'after each' hooks, and 'after all' hooks.

Logging
^^^^^^^

PIRUPY use a logger named 'pipeline_runner'

Requirements on annotaded functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Jobs and hooks functions are provided with a keyword argument `env`, a dictionnary containing resources to
be used to perform the job and the hooks.

The `env` dictionnary is returned by the pipeline function and the hooks. The pipeline function usually create the
dictionnary, whereas hooks functions add ('before all' and 'before each' hooks) or remove ('after all' and 'after each'
hooks) ressources into the dictionnary before returning it.

Typical use
^^^^^^^^^^^

```python
    #... skipping imports, logging config, etc...

    @pipeline(stages=("first_stage","second_stage","third_stage"))
    def performMySuiteOfTests(env:dict = {}):
        logging.info("Start of pipeline -- init")
        logging.debug(env)
        return env

    @job(stage="first_stage")
    def B(*, env:dict = {}):
        logging.info("performing... B")
        pass

    @job(stage="first_stage")
    def A(*, env:dict = {}):
        logging.info("performing... A")
        pass

    @job(stage="second_stage")
    def C(*, env:dict = {}):
        logging.info("performing... C")
        pass

    @job(stage="second_stage")
    def F(*, env:dict = {}):
        logging.info("performing... F")
        pass

    @job(stage="third_stage")
    def E(*, env:dict = {}):
        logging.info("performing... E")
        pass

    @job(stage="second_stage")
    def D(*, env:dict = {}):
        logging.info("performing... D")
        pass

    @job(stage="third_stage")
    def G(*, env:dict = {}):
        logging.info("performing... G")
        pass

    @job()
    def H(*, env:dict = {}): # performed at each stage
        logging.info("performing... H")
        pass

    @before_all
    def setup(*, env:dict = {}):
        logging.info("performing... setup")
        pass

    @after_all
    def teardown(*, env:dict = {}):
        logging.info("performing... teardown")
        pass

    @before_each(stage="first_stage")
    def enter_first_stage_job(*, env:dict = {}): # called only before performing each job of a given stage
        logging.info("performing... enter_first_stage_job")
        pass

    @after_each
    def exit_job(*, env:dict = {}): # called after each jobs has been called during any stage.
        logging.info("performing... exit_job")
        pass

    ### Ready to run
    if __name__ == "__main__":
        logging.warn("before pipeline")
        performMySuiteOfTests(env={'dir.current':'this/path', 'dir.basedir':'that/path'})
        logging.warn("after pipeline")
```

---
(c) 2022 David SPORN
---
This file is part of PIRUPY.

PIRUPY is free software: you can redistribute it and/or modify it under the terms of
the GNU General Public License as published by the Free Software Foundation, either
version 3 of the License, or (at your option) any later version.

PIRUPY is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with PIRUPY.
If not, see <https://www.gnu.org/licenses/>. 
---
"""

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

def _register_func(registry:list, func, stage:str=''):
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
    Annotation to decorate a function that is the entry point to run the pipeline.

    The pipeline is defined by a sequence of 'stages', a stage is just a name to be targeted by jobs and job hooks.

    The annotated function : MUST be unique in the python application ; MUST return a dictionnary with environment
    objects to be used throughout the pipeline, or `None`.

    Parameters
    ==========

    1. _func
        the decorated function.
    ** stages: tuple
        a tuple of stage names (strings).
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
    Annotation to decorate a function that is an actual job for the pipeline.

    A job can be attached to a specific stage, otherwise it is performed at each stage.

    Parameters
    ==========

    1. _func
        the decorated function.
    ** stage: string
        (optionnal)
        the stage name to which this job is attached to.
    """
    LOGGER.debug("Register job")
    def decorator(func):
        def wrapper(*args,**kwargs):
            return func(*args,**kwargs)
        stage = kwargs['stage'] if 'stage' in kwargs else ''
        _register_func(pipeline_jobs, wrapper, stage)
        return wrapper
    if _func is None:
        return decorator
    else:
        return decorator(_func)

def before_all(func):
    """
    Annotation to decorate a function that is called before any job of the pipeline is performed.

    It is intended for setting up environment object that will be shared by all the jobs, e.g. a connection to a database.
    """
    LOGGER.debug(f"Register before_all")
    def wrapper_before_all(* args, **kwargs):
        # before
        # func(kwargs)
        # after
        pass
    result = func
    _register_func(pipeline_before_all, result)
    return result

def after_all(func):
    """
    Annotation to decorate a function that is called after all jobs of the pipeline have been performed.

    It is intended for tearing down environment object shared by all the jobs, e.g. a connection to a database.
    """
    LOGGER.debug(f"Register after_all")
    def wrapper_after_all(* args, **kwargs):
        # before
        # func(kwargs)
        # after
        pass
    result = func
    _register_func(pipeline_after_all, result)
    return result


def before_each(_func=None, *args, **kwargs):
    """
    Annotation to decorate a function that is called before each job of the specified stage, or any jobs when no stage is specified.

    Parameters
    ==========

    1. _func
        the decorated function.
    ** stage: string
        (optionnal)
        the stage name to which this job hook is attached to.
    """
    LOGGER.debug("Register before_each")
    def decorator(func):
        def wrapper(*args,**kwargs):
            return func(*args,**kwargs)
        stage = kwargs['stage'] if 'stage' in kwargs else ''
        _register_func(pipeline_before_each, wrapper, stage)
        return wrapper
    if _func is None:
        return decorator
    else:
        return decorator(_func)

def after_each(_func=None, **kwargs):
    """
    Annotation to decorate a function that is called after each job of the specified stage, or any jobs when no stage is specified.

    Parameters
    ==========

    1. _func
        the decorated function.
    ** stage: string
        (optionnal)
        the stage name to which this job hook is attached to.
    """
    LOGGER.debug("Register after_each")
    def decorator(func):
        def wrapper(*args,**kwargs):
            return func(*args,**kwargs)
        stage = kwargs['stage'] if 'stage' in kwargs else ''
        _register_func(pipeline_after_each, wrapper, stage)
        return wrapper
    if _func is None:
        return decorator
    else:
        return decorator(_func)
