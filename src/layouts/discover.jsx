import { Routes, Route } from "react-router-dom";
import { Cog6ToothIcon } from "@heroicons/react/24/solid";
import { IconButton } from "@material-tailwind/react";
import {
  Sidenav2,
  DashboardNavbar,
  Configurator,
} from "@/widgets/layout";
import routes2 from "@/routes2";
import { useMaterialTailwindController, setOpenConfigurator } from "@/context";

export function Discover() {
  const [controller, dispatch] = useMaterialTailwindController();
  const { sidenavType } = controller;

  return (
    <div className="min-h-screen bg-blue-gray-50/50">
      <Sidenav2
        routes2={routes2}
        brandImg={
          sidenavType === "dark" ? "/img/logo-ct.png" : "/img/logo-ct-dark.png"
        }
      />
      <div className="p-4 xl:ml-80">
        <DashboardNavbar />
        
      </div>
    </div>
  );
}

Discover.displayName = "/src/layout/discover.jsx";

export default Discover;
