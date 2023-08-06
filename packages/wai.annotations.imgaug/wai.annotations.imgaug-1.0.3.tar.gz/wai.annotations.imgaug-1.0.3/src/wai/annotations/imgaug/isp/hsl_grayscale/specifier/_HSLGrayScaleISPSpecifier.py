from typing import Type, Tuple

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import ProcessorStageSpecifier


class HSLGrayScaleISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the hsl-grayscale ISP.
    """
    @classmethod
    def description(cls) -> str:
        return "Turns RGB images into fake grayscale ones by converting them to HSL and then using the L channel for all channels. The brightness can be influenced and varied even."

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.classification import ImageClassificationDomainSpecifier
        from wai.annotations.domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        if input_domain is ImageClassificationDomainSpecifier:
            return input_domain
        elif input_domain is ImageObjectDetectionDomainSpecifier:
            return input_domain
        else:
            raise Exception(
                f"HSLGrayScale only handles the following domains: "
                f"{ImageClassificationDomainSpecifier.name()}, "
                f"{ImageObjectDetectionDomainSpecifier.name()}"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from wai.annotations.imgaug.isp.hsl_grayscale.component import HSLGrayScale
        return HSLGrayScale,
