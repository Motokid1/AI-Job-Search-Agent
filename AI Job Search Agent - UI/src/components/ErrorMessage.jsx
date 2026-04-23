function ErrorMessage({ message }) {
  return (
    <div className="error-box">
      <strong>Error:</strong> {message}
    </div>
  );
}

export default ErrorMessage;
