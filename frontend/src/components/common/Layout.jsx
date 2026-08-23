function Layout({ title, children }) {
  return (
    <div style={{ padding: "30px", maxWidth: "1200px", margin: "0 auto" }}>
      {title && <h1 style={{ marginBottom: "10px", color: "#1b5e20" }}>{title}</h1>}
      <div>{children}</div>
    </div>
  );
}

export default Layout;