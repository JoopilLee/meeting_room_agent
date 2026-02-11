import { useState } from 'react'

async function runAgent(query: string): Promise<{ final_answer: string; success: boolean }> {
  const res = await fetch('/api/run', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || res.statusText)
  }
  return res.json()
}

export default function App() {
  const [query, setQuery] = useState('')
  const [answer, setAnswer] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return
    setLoading(true)
    setError(null)
    setAnswer(null)
    try {
      const data = await runAgent(query.trim())
      setAnswer(data.final_answer ?? '')
    } catch (err) {
      setError(err instanceof Error ? err.message : '요청 실패')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main style={{ width: '100%', maxWidth: 560 }}>
      <h1 style={{ marginBottom: '0.5rem' }}>회의실 에이전트</h1>
      <p style={{ color: '#666', marginBottom: '1.5rem', fontSize: '0.9rem' }}>
        예: 에펠탑 17층 1702-A 오늘 15:00~16:00 비었어?
      </p>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="질문을 입력하세요"
          disabled={loading}
          style={{
            width: '100%',
            padding: '0.75rem 1rem',
            fontSize: '1rem',
            border: '1px solid #ccc',
            borderRadius: 8,
            marginBottom: '0.75rem',
          }}
        />
        <button
          type="submit"
          disabled={loading}
          style={{
            width: '100%',
            padding: '0.75rem',
            fontSize: '1rem',
            background: loading ? '#999' : '#2563eb',
            color: '#fff',
            border: 'none',
            borderRadius: 8,
            cursor: loading ? 'not-allowed' : 'pointer',
          }}
        >
          {loading ? '처리 중…' : '보내기'}
        </button>
      </form>
      {error && (
        <div style={{ marginTop: '1rem', padding: '0.75rem', background: '#fef2f2', color: '#b91c1c', borderRadius: 8 }}>
          {error}
        </div>
      )}
      {answer !== null && (
        <div style={{ marginTop: '1rem', padding: '1rem', background: '#fff', borderRadius: 8, border: '1px solid #e5e7eb', whiteSpace: 'pre-wrap' }}>
          {answer}
        </div>
      )}
    </main>
  )
}
