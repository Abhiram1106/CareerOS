import { AuthState, ProfileState, StateSetter } from "./types";
import { AuthCard } from "./sections/AuthCard";
import { ProfileCard } from "./sections/ProfileCard";

type Props = {
  auth: AuthState;
  setAuth: StateSetter<AuthState>;
  profile: ProfileState;
  setProfile: StateSetter<ProfileState>;
  onRegister: () => Promise<void>;
  onLogin: () => Promise<void>;
  onSaveProfile: () => Promise<void>;
};

export function AccountPane({ auth, setAuth, profile, setProfile, onRegister, onLogin, onSaveProfile }: Props) {
  return (
    <div className="grid pane-grid">
      <AuthCard auth={auth} setAuth={setAuth} onRegister={onRegister} onLogin={onLogin} />
      <ProfileCard profile={profile} setProfile={setProfile} onSaveProfile={onSaveProfile} />
    </div>
  );
}
