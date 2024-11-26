import { z as zod } from 'zod';

import { useState, useMemo } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import Card from '@mui/material/Card';
import Stack from '@mui/material/Stack';
import LoadingButton from '@mui/lab/LoadingButton';
import { paths } from 'src/routes/paths';
import { useRouter } from 'src/routes/hooks';
import { useBoolean } from 'src/hooks/use-boolean';
import { today, fIsAfter } from 'src/utils/format-time';
import { Form } from 'src/components/hook-form';
import { DeclarationNewEditStatusDate } from './declaration-status';
import { DeclarationNewEditDetails } from './declaration-edit-detail';

export const NewInvoiceSchema = zod.object({
  createDate: zod.preprocess(
    (arg) => (typeof arg === 'string' ? new Date(arg) : arg),
    zod.date().optional()
  ),
  items: zod.array(
    zod.object({
      numero: zod.number().min(1, { message: 'Le numero du passeport est obligatoire' }),
      nom: zod.string().min(1, { message: 'Nom est obligatoire!' }),
      nationalite: zod.string().min(1, { message: 'Ce champ est obligatoire!' }),
      fonction: zod.string().min(1, { message: 'Ce champ est obligatoire!' }),
      price: zod.number(),
      total: zod.number(),
    })
  ),
  type: zod.string(),
  status: zod.string(),
  // totalAmount: zod.number(),
  declarationNumber: zod.string(),
});

const generateUniqueId = () => {
  return 'DEC-' + Math.random().toString(36).substr(2, 6).toUpperCase();
};

export function DeclarationNew({ currentInvoice }) {
  const router = useRouter();
  const loadingSave = useBoolean();
  const loadingSend = useBoolean();

  const defaultValues = useMemo(
    () => ({
      declarationNumber: currentInvoice?.declarationNumber || generateUniqueId(),
      createDate: currentInvoice?.createDate || today(),
      status: currentInvoice?.status || 'draft',
      // discount: currentInvoice?.discount || 0,
      //totalAmount: currentInvoice?.totalAmount || 0,
      items: currentInvoice?.items || [
        {
          numero: '',
          nom: '',
          nationalite: '',
          fonction: '',
          type: '',
          price: 0,
          total: 0,
        },
      ],
    }),
    [currentInvoice]
  );

  const methods = useForm({
    mode: 'all',
    resolver: zodResolver(NewInvoiceSchema),
    defaultValues,
  });

  const {
    reset,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  const handleSaveAsDraft = handleSubmit(async (data) => {
    loadingSave.onTrue();

    try {
      await new Promise((resolve) => setTimeout(resolve, 500));
      reset();
      loadingSave.onFalse();
      router.push(paths.dashboard.declaration.list);
      console.info('DATA', JSON.stringify(data, null, 2));
    } catch (error) {
      console.error(error);
      loadingSave.onFalse();
    }
  });

  const handleCreateAndSend = handleSubmit(async (data) => {
    loadingSend.onTrue();

    try {
      await new Promise((resolve) => setTimeout(resolve, 500));
      reset();
      loadingSend.onFalse();
      router.push(paths.dashboard.declaration.list);
      console.info('DATA', JSON.stringify(data, null, 2));
    } catch (error) {
      console.error(error);
      loadingSend.onFalse();
    }
  });

  return (
    <Form methods={methods}>
      <Card>
        <DeclarationNewEditStatusDate />

        <DeclarationNewEditDetails />
      </Card>
      <Stack justifyContent="flex-end" direction="row" spacing={2} sx={{ mt: 3 }}>
        <LoadingButton
          color="inherit"
          size="large"
          variant="outlined"
          loading={loadingSave.value && isSubmitting}
          onClick={handleSaveAsDraft}
        >
          Brouillon
        </LoadingButton>

        <LoadingButton
          size="large"
          variant="contained"
          loading={loadingSend.value && isSubmitting}
          onClick={handleCreateAndSend}
        >
          {currentInvoice ? 'Mettre à jour' : 'Créer'} & Soumettre
        </LoadingButton>
      </Stack>
    </Form>
  );
}
