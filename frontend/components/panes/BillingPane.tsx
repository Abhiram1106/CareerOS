import { Plan } from "./types";
import { CardSection } from "../ui/primitives";

type Props = {
  myPlan: string;
  plans: Plan[];
  onSubscribe: (planCode: string) => Promise<void>;
  onCheckout: (planCode: string, provider: string) => Promise<void>;
};

export function BillingPane({ myPlan, plans, onSubscribe, onCheckout }: Props) {
  return (
    <div className="grid pane-grid">
      <CardSection title="Billing">
        <p className="muted">Current plan: {myPlan}</p>
        {plans.map((p) => (
          <div key={p.code} className="job">
            <strong>{p.name}</strong>
            <p className="muted">INR {p.price_inr_month}/month</p>
            <div className="row">
              <button onClick={() => onSubscribe(p.code)}>Choose {p.code}</button>
              {p.code !== "free" ? <button onClick={() => onCheckout(p.code, "razorpay")}>Checkout Razorpay</button> : null}
              {p.code !== "free" ? <button onClick={() => onCheckout(p.code, "stripe")}>Checkout Stripe</button> : null}
            </div>
          </div>
        ))}
      </CardSection>
      <CardSection title="Phase Progress">
        <p className="muted">Phase 1 core flows are operational, including real payment gateway wiring.</p>
        <p className="muted">Phase 2 modules include ATS history, alerts, tracker, and periodic dispatch scheduling.</p>
        <p className="muted">Next target area is Phase 3 scale surfaces (B2B portal, recruiter module, mobile).</p>
      </CardSection>
    </div>
  );
}
