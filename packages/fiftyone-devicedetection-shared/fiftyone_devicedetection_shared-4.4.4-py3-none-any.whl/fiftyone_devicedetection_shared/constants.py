from fiftyone_pipeline_cloudrequestengine.constants import Constants as CoreConstants

# Class containing values for commonly used evidence keys
class Constants:

    # The suffix that is used to identify a TAC in evidence.
    # https://en.wikipedia.org/wiki/Type_Allocation_Code
    EVIDENCE_TAC_SUFFIX = "tac"

    # The complete key for supplying a TAC as evidence.
    EVIDENCE_QUERY_TAC_KEY = (
        CoreConstants.EVIDENCE_QUERY_PREFIX +
        CoreConstants.EVIDENCE_SEPERATOR +
        EVIDENCE_TAC_SUFFIX)

    # The suffix that is used to identify a native model name in evidence.
    # This is the text returned by 
    # https://developer.android.com/reference/android/os/Build#MODEL 
    # for Android devices and by
    # https://gist.github.com/soapyigu/c99e1f45553070726f14c1bb0a54053b#file-machinename-swift
    # for iOS devices.
    EVIDENCE_NATIVE_MODEL_SUFFIX = "nativemodel"

    # The complete key for supplying a native model name as evidence.
    EVIDENCE_QUERY_NATIVE_MODEL_KEY = (
        CoreConstants.EVIDENCE_QUERY_PREFIX +
        CoreConstants.EVIDENCE_SEPERATOR +
        EVIDENCE_NATIVE_MODEL_SUFFIX)