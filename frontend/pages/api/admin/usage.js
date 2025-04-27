export default async function handler(req, res) {
  const response = await fetch(process.env.NEXT_PUBLIC_BACKEND_URL + '/admin/usage', {
    headers: {
      'Authorization': 'Bearer ' + process.env.NEXT_PUBLIC_ADMIN_TOKEN
    }
  });
  const data = await response.json();
  res.status(200).json(data);
}
