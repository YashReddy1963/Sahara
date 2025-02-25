import {
    HomeIcon,
    UserCircleIcon,
    TableCellsIcon,
    InformationCircleIcon,
  } from "@heroicons/react/24/solid";
  import { Home, Profile, Tables, Notifications } from "@/pages/discover";
  
  const icon = {
    className: "w-5 h-5 text-inherit",
  };
  
  export const routes2 = [
    {
      layout: "discover",
      pages: [
        {
          icon: <HomeIcon {...icon} />,
          name: "home",
          path: "/home",
          element: <Home />,
        },
        {
          icon: <UserCircleIcon {...icon} />,
          name: "profile",
          path: "/profile",
          element: <Profile />,
        },
        {
          icon: <TableCellsIcon {...icon} />,
          name: "tables",
          path: "/tables",
          element: <Tables />,
        },
        {
          icon: <InformationCircleIcon {...icon} />,
          name: "notifications",
          path: "/notifications",
          element: <Notifications />,
        },
      ],
    },
  ];
  
  export default routes2;
  