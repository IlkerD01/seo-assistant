import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';

export default function AdminDashboard() {
  const router = useRouter();
  const [tab, setTab] = useState('payments');
  const [payments, setPayments] = useState([]);
  const [usage, setUsage] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const isAdmin = localStorage.getItem('admin-auth');
    if (!isAdmin) {
      router.push('/admin-login');
    } else {
      fetchPayments();
      fetchUsage();
    }
  }, []);

  const fetchPayments = async () => {
    try {
      const res = await fetch('/api/admin/payments');
      const data = await res.json();
      setPayments(data.payments || []);
    } catch (err) {
      setError('Kan betalingen niet laden.');
    }
  };

  const fetchUsage = async () => {
    try {
      const res = await fetch('/api/admin/usage');
      const data = await res.json();
      setUsage(data.usage || []);
    } catch (err) {
      setError('Kan gebruik logs niet laden.');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Admin Dashboard</h1>
      <div style={{ marginBottom: '20px' }}>
        <button onClick={() => setTab('payments')} style={{ marginRight: '10px' }}>
          Betalingen
        </button>
        <button onClick={() => setTab('usage')}>
          Gebruikersactiviteit
        </button>
      </div>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {tab === 'payments' && (
        <div>
          <h2>Betalingen</h2>
          <table border="1" cellPadding="10" style={{ width: '100%', marginTop: '10px' }}>
            <thead>
              <tr>
                <th>Email</th>
                <th>Bedrag</th>
                <th>Datum</th>
                <th>Status</th>
                <th>Marketing Opt-in</th>
              </tr>
            </thead>
            <tbody>
              {payments.map((payment, idx) => (
                <tr key={idx}>
                  <td>{payment.email}</td>
                  <td>€{payment.amount}</td>
                  <td>{payment.date}</td>
                  <td>{payment.status}</td>
                  <td>{payment.marketing_opt_in ? 'Ja' : 'Nee'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === 'usage' && (
        <div>
          <h2>Gebruikersactiviteit</h2>
          <table border="1" cellPadding="10" style={{ width: '100%', marginTop: '10px' }}>
            <thead>
              <tr>
                <th>Email</th>
                <th>Zoekopdracht</th>
                <th>Tijdstip</th>
              </tr>
            </thead>
            <tbody>
              {usage.map((log, idx) => (
                <tr key={idx}>
                  <td>{log.email}</td>
                  <td>{log.query}</td>
                  <td>{log.timestamp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
