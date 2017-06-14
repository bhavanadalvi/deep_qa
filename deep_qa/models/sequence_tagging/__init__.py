from .verb_semantics_baseline1 import VerbSemanticsBaseline1
from .verb_semantics_baseline2 import VerbSemanticsBaseline2
from .verb_semantics_model_attention import VerbSemanticsModelAttention
from .simple_tagger import SimpleTagger

concrete_models = {  # pylint: disable=invalid-name
        'SimpleTagger': SimpleTagger,
        'VerbSemanticsBaseline1': VerbSemanticsBaseline1,
        'VerbSemanticsBaseline2': VerbSemanticsBaseline2,
        'VerbSemanticsModelAttention': VerbSemanticsModelAttention,
        }
