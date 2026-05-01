function ErrorMessage({ message }) {
  return (
    <div className="error-box">
      <strong>Something went wrong.</strong>
      <span>{message}</span>
    </div>
  );
}

export default ErrorMessage;
