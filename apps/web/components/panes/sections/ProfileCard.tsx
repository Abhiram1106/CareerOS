import { ProfileState, StateSetter } from "../types";
import { CardSection, FormField } from "../../ui/primitives";

type Props = {
  profile: ProfileState;
  setProfile: StateSetter<ProfileState>;
  onSaveProfile: () => Promise<void>;
};

export function ProfileCard({ profile, setProfile, onSaveProfile }: Props) {
  return (
    <CardSection title="Career Profile">
      <FormField label="City"><input value={profile.city} onChange={(e) => setProfile({ ...profile, city: e.target.value })} /></FormField>
      <FormField label="Status">
        <select value={profile.professional_status} onChange={(e) => setProfile({ ...profile, professional_status: e.target.value })}>
          <option>Student</option><option>Fresher</option><option>Experienced</option><option>Career Break</option>
        </select>
      </FormField>
      <FormField label="Target Role"><input value={profile.target_role} onChange={(e) => setProfile({ ...profile, target_role: e.target.value })} /></FormField>
      <FormField label="Skills CSV"><textarea rows={2} value={profile.skills_csv} onChange={(e) => setProfile({ ...profile, skills_csv: e.target.value })} /></FormField>
      <FormField label="Summary"><textarea rows={2} value={profile.summary} onChange={(e) => setProfile({ ...profile, summary: e.target.value })} /></FormField>
      <FormField label="Experience Bullet"><textarea rows={2} value={profile.experience_bullet} onChange={(e) => setProfile({ ...profile, experience_bullet: e.target.value })} /></FormField>
      <button onClick={onSaveProfile}>Save Profile</button>
    </CardSection>
  );
}
