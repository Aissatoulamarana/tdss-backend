import { useEffect, useCallback } from 'react';
import { useFieldArray, useFormContext } from 'react-hook-form';

import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import Divider from '@mui/material/Divider';
import MenuItem from '@mui/material/MenuItem';
import Typography from '@mui/material/Typography';

import { INVOICE_SERVICE_OPTIONS } from 'src/_mock';

import { Field } from 'src/components/hook-form';
import { Iconify } from 'src/components/iconify';

// ----------------------------------------------------------------------

export function DeclarationNewEditDetails() {
  const { control, setValue, watch } = useFormContext();

  const { fields, append, remove } = useFieldArray({ control, name: 'items' });

  const values = watch();

  const handleAdd = () => {
    append({
      numero: '',
      type: 'Nouvelle',
      nom: '',
      fonction: '',
      prenom: '',
      nationalite: '',
    });
  };

  const handleRemove = (index) => {
    remove(index);
  };

  const handleSelectService = useCallback(
    (index, option) => {
      const selectedService = INVOICE_SERVICE_OPTIONS.find((service) => service.name === option);
      if (selectedService) {
        // Vous pouvez ici spécifier explicitement un champ dans votre formulaire si nécessaire
        setValue('serviceField', selectedService); // 'serviceField' est un exemple de champ dans votre formulaire
      }
    },
    [setValue]
  );

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h6" sx={{ color: 'text.disabled', mb: 3 }}>
        Informations Personnelles
      </Typography>

      <Stack divider={<Divider flexItem sx={{ borderStyle: 'dashed' }} />} spacing={3}>
        {fields.map((item, index) => (
          <Stack key={item.id} alignItems="flex-end" spacing={1.5}>
            <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} sx={{ width: 1 }}>
              <Field.Text
                size="small"
                name={`items[${index}].numero`}
                label="Numero Passeport"
                type="number"
                inputlabelprops={{ shrink: true }}
              />
              <Field.Text
                size="small"
                name={`items[${index}].type`}
                label="Type"
                inputlabelprops={{ shrink: true }}
              />
              <Field.CountrySelect
                size="small"
                name={`items[${index}].nationalite`}
                label="Nationalité"
                placeholder="Selectionnez un pays "
                sx={{ width: '100%' }}
                inputlabelprops={{ shrink: true }}
              />

              <Field.Text
                size="small"
                name={`items[${index}].nom`}
                label="Nom "
                inputlabelprops={{ shrink: true }}
              />
              <Field.Text
                size="small"
                name={`items[${index}].prenom`}
                label="Prénom"
                inputlabelprops={{ shrink: true }}
              />

              <Field.Select
                name={`items[${index}].fonction`}
                size="small"
                label="Fonction"
                inputlabelprops={{ shrink: true }}
                sx={{ maxWidth: { md: 160 } }}
              >
                <MenuItem
                  // onClick={() => handleClearService(index)}
                  sx={{ fontStyle: 'italic', color: 'text.secondary' }}
                >
                  None
                </MenuItem>

                <Divider sx={{ borderStyle: 'dashed' }} />

                {INVOICE_SERVICE_OPTIONS.map((service) => (
                  <MenuItem
                    key={service.id}
                    value={service.name}
                    onClick={() => handleSelectService(index, service.name)}
                  >
                    {service.name}
                  </MenuItem>
                ))}
              </Field.Select>
            </Stack>

            <Button
              size="small"
              color="error"
              startIcon={<Iconify icon="solar:trash-bin-trash-bold" />}
              onClick={() => handleRemove(index)}
            >
              Supprimer
            </Button>
          </Stack>
        ))}
      </Stack>

      <Divider sx={{ my: 3, borderStyle: 'dashed' }} />

      <Stack
        spacing={3}
        direction={{ xs: 'column', md: 'row' }}
        alignItems={{ xs: 'flex-end', md: 'center' }}
      >
        <Button
          size="small"
          color="primary"
          startIcon={<Iconify icon="mingcute:add-line" />}
          onClick={handleAdd}
          sx={{ flexShrink: 0 }}
        >
          Add Item
        </Button>
      </Stack>
    </Box>
  );
}
