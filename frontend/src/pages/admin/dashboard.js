import { useEffect } from 'react';
import { useRouter } from 'next/router';

export default function AdminDashboard() {
  const router = useRouter();

  useEffect(() => {
    const isAdmin = localStorage.getItem('admin-auth');
    if (!isAdmin) {
      router.push('/admin-login');
    }
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h1>Welkom op het Admin Dashboard</h1>
      <p>Meer functies komen hier nog...</p>
    </div>
  );
}
