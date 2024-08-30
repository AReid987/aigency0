import { Button } from '@repo/ui/button';

export default function Home() {
  return (
    <div className='min-h-screen bg-black text[#1F2937] py-8'>
      <main>
        <Button appName="web">
          Open alert
        </Button>
      </main>
      <footer>
      </footer>
    </div>
  );
}
