import { NextResponse } from 'next/server';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function GET() {
  try {
    const res = await fetch(`${API_URL}/api/latest`, { cache: 'no-store' });
    if (!res.ok) {
      return NextResponse.json({ error: 'Aucune analyse disponible' }, { status: res.status });
    }
    const data = await res.json();
    return NextResponse.json(data);
  } catch (err) {
    return NextResponse.json({ error: 'Backend indisponible' }, { status: 502 });
  }
}
