import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Target, Users, BookOpen, Settings } from 'lucide-react';
import SopRenderer from './components/SopRenderer';
import './App.css';

const navItems = [
  { id: 'sales', label: 'Sales & Closing', icon: Target, sops: ['inbound-qualification', 'discovery-call', 'proposal-generation'] },
  { id: 'seo', label: 'SEO Operations', icon: LayoutDashboard, sops: ['keyword-research', 'on-page-audit', 'backlink-outreach'] },
  { id: 'marketing', label: 'Marketing', icon: Users, sops: ['content-publishing', 'social-media-sop'] },
  { id: 'operations', label: 'Operations', icon: Settings, sops: ['client-onboarding', 'monthly-reporting'] },
];

function Sidebar() {
  const location = useLocation();

  return (
    <aside className="sidebar">
      <div className="brand">
        <em>system</em><strong>lab.</strong>
      </div>
      
      <div className="nav-section">
        <div className="nav-label">LIBRARY</div>
        <nav>
          {navItems.map(category => {
            const isActive = location.pathname.includes(`/category/${category.id}`);
            return (
              <div key={category.id} className="nav-category">
                <Link to={`/category/${category.id}/${category.sops[0]}`} className={`nav-item ${isActive ? 'active' : ''}`}>
                  <category.icon size={18} />
                  {category.label}
                </Link>
                {isActive && (
                  <div className="sub-nav">
                    {category.sops.map(sop => (
                      <Link 
                        key={sop} 
                        to={`/category/${category.id}/${sop}`}
                        className={`sub-item ${location.pathname.endsWith(sop) ? 'active' : ''}`}
                      >
                        {sop.replace(/-/g, ' ')}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </nav>
      </div>
    </aside>
  );
}

function Dashboard() {
  return (
    <div className="empty-state">
      <BookOpen size={48} className="empty-icon" />
      <h2>Welcome to SystemLab</h2>
      <p>Select a category from the sidebar to view standard operating procedures.</p>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <div className="app-layout">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/category/:categoryId/:sopId" element={<SopRenderer />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}
