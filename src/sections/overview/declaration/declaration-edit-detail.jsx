import { useState, useEffect, useCallback } from 'react';
import { useFieldArray, useFormContext } from 'react-hook-form';

import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import Divider from '@mui/material/Divider';
import MenuItem from '@mui/material/MenuItem';
import Typography from '@mui/material/Typography';
import { Step, Modal, Stepper, StepLabel } from '@mui/material';

import { INVOICE_SERVICE_OPTIONS } from 'src/_mock';

import { Field } from 'src/components/hook-form';
import { Iconify } from 'src/components/iconify';
import { checkPassportExistence } from 'src/services/declaration/api/check-passport';

export function DeclarationNewEditDetails() {
  const { control, setValue, watch } = useFormContext();
  const { fields, append, remove } = useFieldArray({ control, name: 'items' });

  const [openModal, setOpenModal] = useState(false);
  const [activeStep, setActiveStep] = useState(0);

  const values = watch(); // Récupère les valeurs du formulaire en temps réel
  const [passportExists, setPassportExists] = useState(false); // État pour savoir si le passeport existe
  const [passportError, setPassportError] = useState(''); // État pour afficher l'erreur
  const [type, setType] = useState('nouvelle'); // Par défaut, type = nouvelle

  const totalAmount = 0;

  const [rectoImage, setRectoImage] = useState(null);
  const [versoImage, setVersoImage] = useState(null);
  const [signatureImage, setSignatureImage] = useState(null);
  const [empreinteImage, setEmpreinteImage] = useState(null);

  useEffect(() => {
    setValue('totalAmount', totalAmount);
  }, [setValue, totalAmount]);

  const handleAdd = () => {
    append({
      fonction: '',
      nom: '',
      numeroPasseport: '',
      nationalité: '',
    });
  };

  const handleRemove = (index) => {
    remove(index);
  };

  const handleClearService = useCallback(
    (index) => {
      setValue(`items[${index}].quantity`, 1);
      setValue(`items[${index}].price`, 0);
      setValue(`items[${index}].total`, 0);
    },
    [setValue]
  );

  const handleSelectService = useCallback(
    (index, option) => {
      setValue(
        `items[${index}].price`,
        INVOICE_SERVICE_OPTIONS.find((fonction) => fonction.name === option)?.price
      );
      setValue(
        `items[${index}].total`,
        values.items.map((item) => item.quantity * item.price)[index]
      );
    },
    [setValue, values.items]
  );

  const [uploadedImages, setUploadedImages] = useState([]);

  const handleOpenModal = () => {
    setOpenModal(true);
  };

  const handleCloseModal = () => {
    setOpenModal(false);
  };

  const handleNext = () => {
    if (activeStep < 3) {
      setActiveStep((prevStep) => prevStep + 1);
    }
  };

  const handleBack = () => {
    if (activeStep > 0) {
      setActiveStep((prevStep) => prevStep - 1);
    }
  };

  const handleImageUpload = (event, setImage) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleFinish = () => {
    const images = [
      { name: 'Recto', image: rectoImage },
      { name: 'Verso', image: versoImage },
      { name: 'Signature', image: signatureImage },
      { name: 'Empreinte', image: empreinteImage },
    ];

    // Filtrage des images non nulles
    const filteredImages = images.filter((img) => img.image !== null);
    setUploadedImages(filteredImages);

    // Fermeture du modal
    handleCloseModal();
  };

  // Vérifie l'existence du passeport chaque fois que l'utilisateur modifie le champ
  const handlePassportChange = async (event) => {
    const passportNumber = event.target.value;

    // Appel à la fonction d'API pour vérifier si le passeport existe
    try {
      const exists = await checkPassportExistence(passportNumber);
      if (exists) {
        setPassportExists(true);
        setPassportError('Ce numéro de passeport existe déjà.');
        setType('renouvellement'); // Si le passeport existe, le type devient 'renouvellement'
      } else {
        setPassportExists(false);
        setPassportError('');
        setType('nouvelle'); // Si le passeport n'existe pas, le type devient 'nouvelle'
      }
    } catch (error) {
      setPassportError('Erreur lors de la vérification du passeport.');
    }
  };

  // Mettez à jour la valeur du champ 'type' dans votre formulaire
  useEffect(() => {
    setValue('type', type); // Cette ligne met à jour le champ 'type' avec la valeur correcte
  }, [type, setValue]);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h6" sx={{ color: 'text.disabled', mb: 3 }}>
        Informations Personnelles
      </Typography>

      <Stack divider={<Divider flexItem sx={{ borderStyle: 'dashed' }} />} spacing={3}>
        {fields.map((item, index) => (
          <Stack key={item.id} alignItems="flex-end" spacing={1.5}>
            <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} sx={{ width: '100%' }}>
              <Field.Text
                size="small"
                name="numeroPasseport"
                label="Numéro Passeport"
                InputLabelProps={{ shrink: true }}
                sx={{ width: '100%' }}
                onChange={handlePassportChange} // Appel de la fonction de vérification dès que l'utilisateur tape
              />
              {/* Afficher un message d'erreur si le passeport existe déjà */}
              {passportExists && (
                <Typography variant="caption" color="error" sx={{ mt: 1 }}>
                  {passportError}
                </Typography>
              )}

              <Field.Select
                name="type"
                size="small"
                label="Type"
                InputLabelProps={{ shrink: true }}
                sx={{ width: '100%' }}
                value={type} // Le champ "type" est contrôlé par la valeur de `type`
                disabled={passportExists ? false : true} // Si le passeport existe, l'utilisateur peut choisir, sinon il est bloqué
              >
                <MenuItem value="nouvelle" disabled={!passportExists}>
                  Nouvelle
                </MenuItem>
                <MenuItem value="renouvellement" disabled={passportExists}>
                  Renouvellement
                </MenuItem>
                <MenuItem value="duplicata" disabled={passportExists}>
                  Duplicata
                </MenuItem>
              </Field.Select>

              <Field.Text
                size="small"
                name={`items[${index}].nom`}
                label="Nom & Prénom"
                InputLabelProps={{ shrink: true }}
                sx={{ width: '100%' }}
              />

              <Field.CountrySelect
                size="small"
                name="Nationalités"
                label="Nationalités"
                placeholder="Selectionnez un pays "
                sx={{ width: '100%' }}
              />

              <Field.Select
                name={`items[${index}].fonction`}
                size="small"
                label="Fonction"
                InputLabelProps={{ shrink: true }}
                sx={{ width: '80%' }}
              >
                <MenuItem
                  value=""
                  onClick={() => handleClearService(index)}
                  sx={{ fontStyle: 'italic', color: 'text.secondary' }}
                >
                  None
                </MenuItem>
                <Divider sx={{ borderStyle: 'dashed' }} />
                {INVOICE_SERVICE_OPTIONS.map((fonction) => (
                  <MenuItem
                    key={fonction.id}
                    value={fonction.name}
                    onClick={() => handleSelectService(index, fonction.name)}
                  >
                    {fonction.name}
                  </MenuItem>
                ))}
              </Field.Select>
            </Stack>

            <Divider flexItem sx={{ borderStyle: 'solid', my: 2 }} />

            <Button onClick={handleOpenModal} variant="outlined">
              Données Biometriques
            </Button>

            <Divider sx={{ my: 3, borderStyle: 'dashed' }} />

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
          Add item
        </Button>
      </Stack>

      {/* Modal for Biometric Data */}
      <Modal open={openModal} onClose={handleCloseModal}>
        <Box
          sx={{
            width: '60%',
            maxWidth: 600,
            margin: 'auto',
            mt: 10,
            p: 3,
            bgcolor: 'background.paper',
            top: '50%',
            left: '50%',
            transform: 'translate(15%, 60%)',
          }}
        >
          <Stepper activeStep={activeStep} alternativeLabel>
            {['Recto', 'Verso', 'Signature', 'Empreinte'].map((label, i) => (
              <Step key={i}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>

          <Box sx={{ mt: 2 }}>
            <Stack direction="row" justifyContent="space-between" spacing={2}>
              <Button onClick={handleBack} disabled={activeStep === 0}>
                Retour
              </Button>
              <Button onClick={activeStep === 3 ? handleFinish : handleNext}>
                {activeStep === 3 ? 'Terminer' : 'Suivant'}
              </Button>
            </Stack>

            <Box sx={{ mt: 2 }}>
              <Typography variant="h6" align="center">
                {['Recto', 'Verso', 'Signature', 'Empreinte'][activeStep]}
              </Typography>

              {/* Display current uploaded image */}
              {activeStep === 0 && rectoImage && (
                <img
                  src={rectoImage}
                  type="file"
                  accept="image/*"
                  alt="Recto"
                  style={{ width: '100%', height: 'auto' }}
                />
              )}
              {activeStep === 1 && versoImage && (
                <img
                  src={versoImage}
                  type="file"
                  accept="image/*"
                  alt="Verso"
                  style={{ width: '100%', height: 'auto' }}
                />
              )}
              {activeStep === 2 && signatureImage && (
                <img
                  src={signatureImage}
                  type="file"
                  accept="image/*"
                  alt="Signature"
                  style={{ width: '100%', height: 'auto' }}
                />
              )}
              {activeStep === 3 && empreinteImage && (
                <img
                  src={empreinteImage}
                  type="file"
                  accept="image/*"
                  alt="Empreinte"
                  style={{ width: '100%', height: 'auto' }}
                />
              )}

              {/* File upload input for each step */}
              {activeStep === 0 && (
                <Field.UploadAvatar
                  name="rectoImage"
                  maxSize={3145728}
                  helperText={
                    <Typography variant="caption">Allowed *.jpeg, *.jpg, *.png, *.gif</Typography>
                  }
                  onChange={handleImageUpload}
                />
              )}
              {activeStep === 1 && (
                <Field.UploadAvatar
                  name="versoImage"
                  maxSize={3145728}
                  helperText={
                    <Typography variant="caption">Allowed *.jpeg, *.jpg, *.png, *.gif</Typography>
                  }
                  onChange={handleImageUpload}
                />
              )}
              {activeStep === 2 && (
                <Field.UploadAvatar
                  name="signatureImage"
                  maxSize={3145728}
                  helperText={
                    <Typography variant="caption">Allowed *.jpeg, *.jpg, *.png, *.gif</Typography>
                  }
                  onChange={handleImageUpload}
                />
              )}
              {activeStep === 3 && (
                <Field.UploadAvatar
                  name="empreinteImage"
                  maxSize={3145728}
                  helperText={
                    <Typography variant="caption">Allowed *.jpeg, *.jpg, *.png, *.gif</Typography>
                  }
                  onChange={handleImageUpload}
                />
              )}
            </Box>
          </Box>
        </Box>
      </Modal>

      {/* Display uploaded images */}
      {uploadedImages.length > 0 && (
        <Box sx={{ mt: 3 }}>
          <Typography variant="h6">Images téléchargées</Typography>
          <Stack direction="row" spacing={2}>
            {uploadedImages.map((img, index) => (
              <Box key={index} sx={{ textAlign: 'center' }}>
                <Typography variant="caption">{img.name}</Typography>
                <Field.UploadAvatar
                  name={`${img.name.toLowerCase()}Image`}
                  maxSize={3145728}
                  helperText={
                    <Typography variant="caption">Allowed *.jpeg, *.jpg, *.png, *.gif</Typography>
                  }
                  value={img.image}
                  readOnly
                />
              </Box>
            ))}
          </Stack>
        </Box>
      )}
    </Box>
  );
}
