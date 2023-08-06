from django.core.exceptions import PermissionDenied
from .apps import CALCULATION_RULES
from .calculation_rule import ContributionValuationRule


def get_rule_name(class_name):
    list_rule_name = []
    for calculation_rule in CALCULATION_RULES:
        result_signal = calculation_rule.signal_get_rule_name.send(sender=class_name, class_name=class_name)
        if result_signal:
            list_rule_name.extend(result_signal)
    return list_rule_name


def get_rule_details(class_name):
    list_rule_details = []
    for calculation_rule in CALCULATION_RULES:
        result_signal = calculation_rule.signal_get_rule_details.send(sender=class_name, class_name=class_name)
        if result_signal:
            list_rule_details.extend(result_signal)
    return list_rule_details


def run_calculation_rules(instance, context, user, **kwargs):
    for calculation_rule in CALCULATION_RULES:
        result_signal = calculation_rule.signal_calculate_event.send(
            sender=instance.__class__.__name__, instance=instance, user=user, context=context, **kwargs
        )
        if result_signal[0][1]:
            return result_signal
    # if no listened calculation rules - return None
    return None


def get_parameters(class_name, instance):
    """ className is the class name of the object where the calculation param need to be added
        instance is where the link with a calculation need to be found,
         like the CPB in case of PH insuree or Contract Details
    """
    list_parameters = []
    for calculation_rule in CALCULATION_RULES:
        result_signal = calculation_rule.signal_get_param.send(
            sender=instance, class_name=class_name, instance=instance
        )
        if result_signal:
            list_parameters.extend(result_signal)
    # return the ruleDetails that are valid to classname and related to instance
    return list_parameters


def get_linked_class(class_name_list=None):
    return_list_class = []
    for calculation_rule in CALCULATION_RULES:
        if class_name_list == None:
            result_signal = calculation_rule.signal_get_linked_class.send(sender="None", class_name=None)
            if result_signal:
                return_list_class.extend(result_signal)
        else:
            for class_name in class_name_list:
                result_signal = calculation_rule.signal_get_linked_class.send(sender=class_name, class_name=class_name)
                if result_signal:
                    return_list_class.extend(result_signal)
    return return_list_class
