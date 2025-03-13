import { useState } from "react";
import { Card, Input, Button, Typography } from "@material-tailwind/react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

export function SignUp() {
  const navigate = useNavigate();
  const [userType, setUserType] = useState("user");

  return (
    <section className="m-8 flex">
      <div className="w-2/5 h-full hidden lg:block">
        <img
          src="/img/together.jpg"
          className="h-full w-full object-cover rounded-3xl"
        />
      </div>
      <div className="w-full lg:w-3/5 flex flex-col items-center justify-center">
        <div className="text-center">
          <Typography variant="h2" className="font-bold mb-4">
            Join Us Today
          </Typography>
          <Typography variant="paragraph" color="blue-gray" className="text-lg font-normal">
            Select your role and enter your details to register.
          </Typography>

          <div className="mt-4 w-80">
            <Typography variant="small" color="blue-gray" className="font-medium">
              Select Type
            </Typography>
            <select
              className="w-full border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900"
              value={userType}
              onChange={(e) => setUserType(e.target.value)}
            >
              <option value="user">User</option>
              <option value="ngo">NGO</option>
            </select>
          </div>
        </div>

        {/* Registration Form */}
        <form className="mt-8 mb-2 mx-auto w-80 max-w-screen-lg lg:w-1/2">
          <div className="mb-1 flex flex-col gap-6">
            {userType === "user" ? (
              <>
                <Typography variant="small" color="blue-gray" className="-mb-3 font-medium">
                  Your Name
                </Typography>
                <Input name="username" size="lg" placeholder="Username"/>

                <Typography variant="small" color="blue-gray" className="-mb-3 font-medium">
                  Your Email
                </Typography>
                <Input name="email" size="lg" placeholder="name@mail.com"/>

                <Typography variant="small" color="blue-gray" className="-mb-3 font-medium">
                  Password
                </Typography>
                <Input name="password" size="lg" type="password" placeholder="Password"/>

                <Typography variant="small" color="blue-gray" className="-mb-3 font-medium">
                  Contact No.
                </Typography>
                <Input name="contact_number" size="lg" placeholder="Phone Number"/>

                <Typography variant="small" color="blue-gray" className="-mb-3 font-medium">
                  Your Picture
                </Typography>
                <Input name="profile_picture" size="lg" type="file"/>

                <Button className="mt-6" type="submit" fullWidth>
                  Register Now
                </Button>
              </>
            ) : (
              <>
                <Typography variant="small" color="blue-gray" className="-mb-3 font-medium">
                  NGO Name
                </Typography>
                <Input name="organization_name" size="lg" placeholder="NGO Name"/>

                <Typography variant="small" color="blue-gray" className="-mb-3 font-medium">
                  Type of NGO
                </Typography>
                <Input name="type_of_ngo" size="lg" placeholder="Working for which sector"/>

                <Typography variant="small" color="blue-gray" className="-mb-3 font-medium">
                  Authority Person
                </Typography>
                <Input name="organization_authority_name" size="lg" placeholder="Contact Person Name"/>

                <Typography variant="small" color="blue-gray" className="-mb-3 font-medium">
                  Government Registered Id
                </Typography>
                <Input name="government_issued_id" size="lg" placeholder="Enter Government Id"/>

                <Typography variant="small" color="blue-gray" className="-mb-3 font-medium">
                  Email
                </Typography>
                <Input name="email" size="lg" placeholder="ngo@mail.com"/>

                <Typography variant="small" color="blue-gray" className="-mb-3 font-medium">
                  Password
                </Typography>
                <Input name="password" size="lg" placeholder="e.g, Password@123"/>

                <Typography variant="small" color="blue-gray" className="-mb-3 font-medium">
                  Password
                </Typography>
                <Input name="password" size="lg" placeholder="e.g, Password@123"/>

                <Typography variant="small" color="blue-gray" className="-mb-3 font-medium">
                  Profile/Logo
                </Typography>
                <Input name="profile_picture" size="lg" type="file"/>

                <Typography variant="small" color="blue-gray" className="-mb-3 font-medium">
                  Contact No.
                </Typography>
                <Input name="contact_number" size="lg" placeholder="Phone Number"/>

                <Typography variant="small" color="blue-gray" className="-mb-3 font-medium">
                  Address
                </Typography>
                <Input name="address" size="lg" placeholder="Location of NGO"/>

                <Typography variant="small" color="blue-gray" className="-mb-3 font-medium">
                  Social Link
                </Typography>
                <Input name="social_link" size="lg" placeholder="Social profile link"/>

                <Button className="mt-6" type="submit" fullWidth>
                  Register Now
                </Button>
              </>
            )}

            <Typography variant="paragraph" className="text-center text-blue-gray-500 font-medium mt-4">
              Already have an account?
              <Link to="/sign-in" className="text-gray-900 ml-1">
                Sign in
              </Link>
            </Typography>
          </div>
        </form>
      </div>
    </section>
  );
}

export default SignUp;
