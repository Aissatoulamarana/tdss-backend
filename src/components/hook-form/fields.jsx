import { RHFSelect } from './rhf-select';
import { RHFTextField } from './rhf-text-field';
import { RHFCountrySelect } from './rhf-country-select';
import { RHFUpload, RHFUploadBox, RHFUploadAvatar } from './rhf-upload';
import { RHFDatePicker, RHFMobileDateTimePicker } from './rhf-date-picker';
import { RHFSwitch, RHFMultiSwitch } from './rhf-switch';
import { RHFPhoneInput } from './rhf-phone-input';
// ----------------------------------------------------------------------

export const Field = {
  Text: RHFTextField,
  Select: RHFSelect,
  MobileDateTimePicker: RHFMobileDateTimePicker,
  DatePicker: RHFDatePicker,
  UploadBox: RHFUploadBox,
  UploadAvatar: RHFUploadAvatar,
  Upload: RHFUpload,
  CountrySelect: RHFCountrySelect,
  Switch: RHFSwitch,
  Phone: RHFPhoneInput,
};
