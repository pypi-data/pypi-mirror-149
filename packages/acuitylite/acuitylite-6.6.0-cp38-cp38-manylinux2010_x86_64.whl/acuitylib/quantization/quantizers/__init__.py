from acuitylib.quantization.quantizers.quantizer_impl import QuantizerImpl
from acuitylib.quantization.quantizers.float16_quantizer import *
from acuitylib.quantization.quantizers.bfloat16_quantizer import *
from acuitylib.quantization.quantizers.dynamic_fixed_point_quantizer import *
from acuitylib.quantization.quantizers.symmetric_quantizer import *
from acuitylib.quantization.quantizers.asymmetric_quantizer import *
from acuitylib.quantization.quantizers.perchannel_symmetric_quantizer import *
from acuitylib.quantization.quantizers.perchannel_asymmetric_quantizer import *


def get_quantizer(quantizer_name : str) -> QuantizerImpl:
    from acuitylib.quantization.types import QuantizerType
    _quantizers = {
        QuantizerType.DYNAMIC_FIXED_POINT: DynamicFixedPointQuantizer,
        QuantizerType.ASYMMETRIC_AFFINE: AsymmetricQuantizer,
        QuantizerType.SYMMETRIC_AFFINE: SymmetricQuantizer,
        QuantizerType.PERCHANNEL_SYMMETRIC_AFFINE: PerchannelSymmetricQuantizer,
        QuantizerType.PERCHANNEL_ASYMMETRIC_AFFINE: PerchannelAsymmetricQuantizer,
        # QBFLOAT16 == BFLOAT16
        QuantizerType.BFLOAT16: BFloat16Quantizer,
        QuantizerType.FLOAT16: Float16Quantizer,
    }
    return _quantizers.get(quantizer_name, None)
