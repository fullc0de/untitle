export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="card w-96 bg-base-100 shadow-xl">
        <div className="card-body items-center text-center">
          <h1 className="card-title text-4xl font-bold">환영합니다</h1>
          <p className="text-xl">Next.js와 Tailwind CSS로 만든 애플리케이션입니다.</p>
          <div className="card-actions justify-end">
            <button className="btn btn-primary">시작하기</button>
          </div>
        </div>
      </div>
    </main>
  );
} 