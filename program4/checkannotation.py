# Submitter: haininz(Zhou, Haining)
# Partner:   clyu4(Lyu, Chenhan)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming
from goody import type_as_str
import inspect


class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """

    def __init__(self, *args):
        self._annotations = args

    def __repr__(self):
        return 'Check_All_OK(' + ','.join([str(i) for i in self._annotations]) + ')'

    def __check_annotation__(self, check, param, value, check_history):
        for annot in self._annotations:
            check(param, annot, value,
                  check_history + 'Check_All_OK check: ' + str(annot) + ' while trying: ' + str(self) + '\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """

    def __init__(self, *args):
        self._annotations = args

    def __repr__(self):
        return 'Check_Any_OK(' + ','.join([str(i) for i in self._annotations]) + ')'

    def __check_annotation__(self, check, param, value, check_history):
        failed = 0
        for annot in self._annotations:
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param) + ' failed annotation check(Check_Any_OK): value = ' + repr(value) + \
                          '\n  tried ' + str(self) + '\n' + check_history


class Check_Annotation:
    # To begin, by binding the class attribute to True means checking can occur
    #   (but only when self._checking_on is bound to True too)
    checking_on = True

    # For checking the decorated function, bind self._checking_on as True too
    def __init__(self, f):
        self._f = f
        self._checking_on = True

    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self, param, annot, value, check_history=''):
        def _check_list_tuple(param, annot, value, check_history):
            assert type(value) is type(
                annot), f"'{param}' failed annotation check(wrong type): value = {value}\n  was type {type_as_str(value)} ...should be type {str(type(annot))[8:-2]}\n" + check_history
            if len(annot) == 1:
                for i in value:
                    self.check(param, annot[0], i, check_history+str(type(annot))[8:-2]+'['+str(value.index(i))+'] check: '+str(annot[0])+ '\n')
            else:
                assert len(value) == len(
                    annot), f'{param} failed annotation check(wrong number of elements): value = {value}\n  annotation had {len(annot)} elements{annot}\n' + check_history
                for k, v in zip(annot, value):
                    self.check(param, k, v, check_history+str(type(annot))[8:-2]+'['+str(value.index(v))+'] check: '+str(k)+ '\n')

        def _check_dict(param, annot, value, check_history):
            assert isinstance(value,
                              dict), f"'{param}' failed annotation check(wrong type): value = {value}\n  was type {type_as_str(value)} ...should be type dict\n" + check_history
            assert len(
                annot) == 1, f'{param} failed annotation check(wrong number of elements): value = {value}\n  annotation had {len(annot)} elements{annot}\n' + check_history
            for i, j in annot.items():
                key, keyvalue = i, j
            for k, v in value.items():
                self.check(param, key, k, check_history + 'dict key check: '+ str(key)+'\n')
                self.check(param, keyvalue, v, check_history + 'dict value check: '+ str(keyvalue)+'\n')

        def _check_sets(param, annot, value, check_history):
            assert type(value) is type(
                annot), f"'{param}' failed annotation check(wrong type): value = {value}\n  was type {type_as_str(value)} ...should be type set\n" + check_history
            assert len(
                annot) == 1, f'{param} annotation inconsistency: set should have 1 value but had {len(annot)}\n  annotation = {annot}\n' + check_history
            inner_type = next(iter(annot))
            for i in value:
                self.check(param, inner_type, i, check_history + 'set value check: ' + str(inner_type) + '\n')

        def _check_lambda(param, annot, value, check_history):
            Error = None
            Error_message = None
            assert len(inspect.signature(
                annot).parameters) == 1, f"{param} annotation inconsistency: predicate should have 1 parameter but had {len(inspect.signature(annot).parameters)}\n  predicate = {annot}\n" + check_history
            try:
                assert annot(value)
            except AssertionError:
                raise AssertionError(f'{param} failed annotation check: value = {value}\n  predicate = {annot}\n' + check_history)
            except Exception as e:
                Error = e
                Error_message = str(e)
            finally:
                if Error != None:
                    raise AssertionError(
                        f"'{param}' annotation predicate({annot}) raised exception\n  exception = TypeError: {Error_message}\n" + check_history)

        def _check_string(param, annot, value, check_history):
            Error = None
            Error_message = None
            answer = annot
            eval_list = []
            for k,v in self.pa_dict.items():
                if k in answer:
                    if type(v) is not str:
                        answer = answer.replace(k,str(v))
                    else:
                        answer = answer.replace(k,"'"+v+"'")
                    eval_list.append(f'{k}->{str(v)}')
            try:
                if not eval(answer):
                    raise AssertionError
            except AssertionError:
                raise AssertionError(f"'{param}' failed annotation check(str predicate: '{annot}')\n  args for evaluation: {', '.join(eval_list)}\n" + check_history)
            except Exception as e:
                Error = e
                Error_message = str(e)
            finally:
                if Error != None:
                    raise AssertionError(
                        f"'{param}' annotation check(str predicate: '{annot}') raised exception\n  exception = TypeError: {Error_message}\n" + check_history)

        if annot is None:
            pass
        elif type(annot) is type:
            if type(value) is str:
                assert type(
                    value) is annot, f"'{param}' failed annotation check(wrong type): value = '{value}'\n  was type {type_as_str(value)} ...should be type {str(annot)[8:-2]}\n" + check_history
            else:
                assert type(
                    value) is annot, f"'{param}' failed annotation check(wrong type): value = {value}\n  was type {type_as_str(value)} ...should be type {str(annot)[8:-2]}\n" + check_history
        elif isinstance(annot, list):
            _check_list_tuple(param, annot, value, check_history)
        elif isinstance(annot, tuple):
            _check_list_tuple(param, annot, value, check_history)
        elif isinstance(annot, dict):
            _check_dict(param, annot, value, check_history)
        elif isinstance(annot, set):
            _check_sets(param, annot, value, check_history)
        elif isinstance(annot, frozenset):
            _check_sets(param, annot, value, check_history)
        elif type_as_str(annot) == "function":
            _check_lambda(param, annot, value, check_history)
        elif type(annot) is str:
            _check_string(param, annot, value, check_history)
        else:
            Error_message = None
            Error = None
            try:
                annot.__check_annotation__(self.check, param, value, check_history + f'{str(type(annot))[8:-2]} value check: '+ str(type(value)) + '\n')
            except AttributeError as e:
                Error = AttributeError
                Error_message = str(e)
            except AssertionError as e:
                Error = AssertionError
                Error_message = str(e)
            except Exception as e:
                Error = e
                Error_message = str(e)
            finally:
                if Error != None:
                    if Error == AttributeError:
                        raise AssertionError(f"'{param}' annotation undecipherable: {annot}")
                    elif Error == AssertionError:
                        raise AssertionError(Error_message + check_history)
                    else:
                        raise AssertionError(f"'{param}' annotation raised exception\n  exception = {Error_message}" + check_history)
    # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)

        # To begin, get check's function annotation and compare it to its arguments

    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        # Return an ordereddict of the parameter/argument bindings: it's a special
        #   kind of dict, binding the function header's parameters in order
        def param_arg_bindings():
            f_signature = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args, **kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking

        try:
            # Check the annotation for each of the parameters that is annotated             
            if not Check_Annotation.checking_on or not self._checking_on:
                return self._f(*args)
            self.pa_dict = param_arg_bindings()
            annotation_dict = self._f.__annotations__
            for i in self.pa_dict:
                if i in annotation_dict:
                    if annotation_dict[i]:
                        self.check(i, annotation_dict[i], self.pa_dict[i])
            #                         assert type(pa_dict[i]) == annotation_dict[i]
            # Compute/remember the value of the decorated function
            f_return = self._f(*args)
            self.pa_dict['_return'] = f_return
            # If 'return' is in the annotation, check it
            if 'return' in annotation_dict:
                self.check('return', annotation_dict['return'], self.pa_dict['_return'])
            #                 assert annotation_dict['_return'] == annotation_dict['return']
            # Return the decorated answer
            return f_return
            # remove after adding real code in try/except

        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
            # print(80*'-')
            # for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
            #     print(l.rstrip())
            # print(80*'-')
            raise


if __name__ == '__main__':
    # an example of testing a simple annotation
    # driver tests
    import driver

    driver.default_file_name = 'bscp4F19.txt'
    # driver.default_show_exception= True
    # driver.default_show_exception_message= True
    # driver.default_show_traceback= True
    driver.driver()
