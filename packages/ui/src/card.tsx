/**
 * Renders a card component with a title, content, and a link.
 * @param {Object} props - The properties for the Card component.
 * @param {string} [props.className] - Optional CSS class name for additional styling.
 * @param {string} props.title - The title of the card.
 * @param {React.ReactNode} props.children - The content of the card.
 * @param {string} props.href - The URL that the card links to.
 * @returns {JSX.Element} A JSX element representing the card.
 */
export function Card({
  className,
  title,
  children,
  href,
}: {
  className?: string;
  title: string;
  children: React.ReactNode;
  href: string;
}): JSX.Element {
  return (
    <a
      className={className}
      href={`${href}?utm_source=create-turbo&utm_medium=basic&utm_campaign=create-turbo"`}
      rel="noopener noreferrer"
      target="_blank"
    >
      <h2>
        {title} <span>-&gt;</span>
      </h2>
      <p>{children}</p>
    </a>
  );
}
