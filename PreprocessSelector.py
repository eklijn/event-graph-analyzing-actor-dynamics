from preprocessors.BPIC2017Preprocessor import BPIC2017Preprocessor
from preprocessors.BPIC2014Preprocessor import BPIC2014Preprocessor
from preprocessors.GeneralPreprocessor import GeneralPreprocessor


def get_preprocessor(dataset, filename, column_names, separator, timestamp_format, path_to_neo4j_import_directory):
    if dataset in ["bpic2017_single_ek", "bpic2017_single_ek_filtered", "bpic2017_case_attr", "bpic2017_susp_res"]:
        return BPIC2017Preprocessor(name_data_set=dataset, filename=filename, column_names=column_names,
                                    separator=separator, timestamp_format=timestamp_format,
                                    path_to_neo4j_import_directory=path_to_neo4j_import_directory)
    elif dataset == ["bpic2014_single_ek"]:
        return BPIC2014Preprocessor(name_data_set=dataset, filename=filename, column_names=column_names,
                                    separator=separator, timestamp_format=timestamp_format,
                                    path_to_neo4j_import_directory=path_to_neo4j_import_directory)
    else:
        return GeneralPreprocessor(name_data_set=dataset, filename=filename, column_names=column_names,
                                   separator=separator, timestamp_format=timestamp_format,
                                   path_to_neo4j_import_directory=path_to_neo4j_import_directory)
