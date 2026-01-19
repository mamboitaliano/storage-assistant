import { NavLink, Outlet } from 'react-router-dom';
import { Package, Box, Home, Layers, Search } from 'lucide-react';

const navItems = [
  { to: '/items', label: 'Items', icon: Package },
  { to: '/containers', label: 'Containers', icon: Box },
  { to: '/rooms', label: 'Rooms', icon: Home },
  { to: '/floors', label: 'Floors', icon: Layers },
];

export default function Layout() {
  return (
    <div className="h-screen flex flex-col overflow-hidden">
      {/* Top Navbar */}
      <header 
        className="sticky top-0 z-50 h-14 flex-shrink-0 flex items-center justify-between px-6 border-b"
        style={{ 
          backgroundColor: 'var(--gunmetal-900)', 
          borderColor: 'var(--gunmetal-700)' 
        }}
      >
        <h1 
          className="text-lg font-semibold tracking-tight"
          style={{ color: 'var(--gunmetal-300)' }}
        >
          Storage Assistant
        </h1>
        
        <div className="flex items-center gap-3">
          <span 
            className="text-sm hidden sm:block"
            style={{ color: 'var(--gunmetal-500)' }}
          >
            Find something
          </span>
          <div className="relative">
            <Search 
              size={16} 
              className="absolute left-3 top-1/2 -translate-y-1/2"
              style={{ color: 'var(--gunmetal-500)' }}
            />
            <input
              type="text"
              placeholder="Search..."
              className="pl-9 pr-4 py-1.5 text-sm rounded-md w-48 focus:outline-none focus:ring-2 transition-all"
              style={{ 
                backgroundColor: 'var(--gunmetal-800)',
                borderColor: 'var(--gunmetal-700)',
                color: 'var(--gunmetal-300)',
              }}
            />
          </div>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar */}
        <aside 
          className="w-56 border-r flex-shrink-0 overflow-hidden"
          style={{ 
            backgroundColor: 'var(--gunmetal-900)', 
            borderColor: 'var(--gunmetal-700)' 
          }}
        >
          <nav className="p-3 space-y-1">
            {navItems.map(({ to, label, icon: Icon }) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive ? 'active-nav' : 'inactive-nav'
                  }`
                }
                style={({ isActive }) => ({
                  backgroundColor: isActive ? 'var(--gunmetal-800)' : 'transparent',
                  color: isActive ? 'var(--accent)' : 'var(--gunmetal-400)',
                })}
              >
                <Icon size={18} />
                {label}
              </NavLink>
            ))}
          </nav>
        </aside>

        {/* Main Content */}
        <main 
          className="flex-1 p-6 overflow-auto"
          style={{ backgroundColor: 'var(--gunmetal-950)' }}
        >
          <Outlet />
        </main>
      </div>
    </div>
  );
}