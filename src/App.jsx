import { Routes, Route, Navigate } from "react-router-dom";
import { Dashboard, Main, Discover } from "@/layouts";
import { SignIn, SignUp, OTP } from "@/pages/auth";
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <Routes>
      <Route path="/sign-up" element={<SignUp />} />
      <Route path="/sign-in" element={<SignIn />} />
      <Route path="/otp" element={<OTP />} />
      <Route path="/dashboard/*" element={<Dashboard />} />
      <Route path="/discover/*" element={<Discover />} />
      <Route path="/" element={<Main />}/>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
