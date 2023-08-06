from ts_t1_validator.models.enums.media_type import MediaTypeEnum
from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule


class MediaTypeRule(ValidationRule):
    def __init__(self, media_type: MediaTypeEnum):
        self.media_type = media_type

    def execute(self):
        """
        media_type should be kind of valid enumeration
        """

        if self.media_type is MediaTypeEnum.UNDEFINED:
            raise ValidationException("media_type must be one of " + str(MediaTypeEnum.asList()))
