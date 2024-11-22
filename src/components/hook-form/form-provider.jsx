import { useForm } from 'react-hook-form';
import { Form } from './Form';

function LoginForm() {
  const methods = useForm({
    defaultValues: { email: '', password: '' },
  });

  const onSubmit = (data) => {
    console.log('Form Data:', data);
  };

  return (
    <Form onSubmit={onSubmit} methods={methods}>
      <input {...methods.register('email')} placeholder="Email" />
      <input {...methods.register('password')} type="password" placeholder="Password" />
      <button type="submit">Submit</button>
    </Form>
  );
}