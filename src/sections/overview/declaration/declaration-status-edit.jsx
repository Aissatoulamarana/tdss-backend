import { useFormContext } from 'react-hook-form';
import { useState } from 'react';
import Stack from '@mui/material/Stack';
import MenuItem from '@mui/material/MenuItem';

import { Field } from 'src/components/hook-form';

// ----------------------------------------------------------------------

export function DeclarationEditStatusDate() {
  const { watch } = useFormContext();

  const values = watch();

  return (
    <Stack
      spacing={2}
      direction={{ xs: 'column', sm: 'row' }}
      sx={{ p: 3, bgcolor: 'background.neutral' }}
    >
      <Field.Text
        disabled
        name={`items[${index}].declarationNumber`}
        label="Numero de la declaration"
        value={values.declarationNumber}
      />

      <Field.Select
        fullWidth
        name="status"
        label="Status"
        InputLabelProps={{ shrink: true }}
        disabled
      >
        {['paid', 'pending', 'overdue', 'draft'].map((option) => (
          <MenuItem key={option} value={option} sx={{ textTransform: 'capitalize' }}>
            {option}
          </MenuItem>
        ))}
      </Field.Select>

      <Field.DatePicker name={`items[${index}].createDate`} label="Date" disabled />
    </Stack>
  );
}
