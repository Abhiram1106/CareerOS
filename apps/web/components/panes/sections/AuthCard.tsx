import { AuthState, StateSetter } from "../types";
import { CardSection, FormField } from "../../ui/primitives";

type Props = {
  auth: AuthState;
  setAuth: StateSetter<AuthState>;
  onRegister: () => Promise<void>;
  onLogin: () => Promise<void>;
};

export function AuthCard({ auth, setAuth, onRegister, onLogin }: Props) {
  return (
    <CardSection title="Authentication">
      <FormField label="Full Name"><input value={auth.full_name} onChange={(e) => setAuth({ ...auth, full_name: e.target.value })} /></FormField>
      <FormField label="Email"><input value={auth.email} onChange={(e) => setAuth({ ...auth, email: e.target.value })} /></FormField>
      <FormField label="Password"><input type="password" value={auth.password} onChange={(e) => setAuth({ ...auth, password: e.target.value })} /></FormField>
      <div className="row"><button onClick={onRegister}>Register</button><button onClick={onLogin}>Login</button></div>
    </CardSection>
  );
}
