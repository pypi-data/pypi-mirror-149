from typing import Type, Tuple

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import ProcessorStageSpecifier


class LinearContrastISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the linear contrast image ISP.
    """
    @classmethod
    def description(cls) -> str:
        return "Applies linear contrast to images."

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
                f"LinearContrast only handles the following domains: "
                f"{ImageClassificationDomainSpecifier.name()}, "
                f"{ImageObjectDetectionDomainSpecifier.name()}"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from wai.annotations.imgaug.isp.linear_contrast.component import LinearContrast
        return LinearContrast,
