import java.sql.*;
public class OrderProcessor {
    public static void main(String[] args) throws Exception {
        String dbUrl = "jdbc:sqlite:../pharmacy.db";
        Class.forName("org.sqlite.JDBC");
        try (Connection conn = DriverManager.getConnection(dbUrl)){
            String q = "SELECT id, user_id, total, status FROM orders WHERE status='pending'";
            try (PreparedStatement ps = conn.prepareStatement(q); ResultSet rs = ps.executeQuery()){
                while(rs.next()){
                    int id = rs.getInt("id");
                    System.out.println("Processing order: " + id);
                    try (PreparedStatement upd = conn.prepareStatement("UPDATE orders SET status='processed' WHERE id=?")){
                        upd.setInt(1, id);
                        upd.executeUpdate();
                    }
                }
            }
        }
    }
}
