from variant_encoders.BPIC2017VariantEncoder import BPIC2017VariantEncoder
from variant_encoders.GeneralVariantEncoder import GeneralEncoder


def get_variant_encoder(name_data_set, merge_events=False, event_priority="A_OW", use_count=False):

    if name_data_set == "bpic2017":
        return BPIC2017VariantEncoder(merge_events, event_priority, use_count)
    else:
        return GeneralEncoder()
