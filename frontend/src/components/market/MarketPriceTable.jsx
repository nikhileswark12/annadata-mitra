import {
  Card,
  CardContent,
  Typography,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  TableContainer,
} from "@mui/material";

function MarketPriceTable({ prices }) {
  if (!prices || prices.length === 0) return null;

  return (
    <Card elevation={3} sx={{ borderRadius: 3 }}>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
          Market Price Table
        </Typography>

        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell><strong>Market</strong></TableCell>
                <TableCell><strong>Crop</strong></TableCell>
                <TableCell><strong>Price</strong></TableCell>
                <TableCell><strong>Distance</strong></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {prices.map((item, index) => (
                <TableRow key={index}>
                  <TableCell>{item.market}</TableCell>
                  <TableCell>{item.crop}</TableCell>
                  <TableCell>₹{item.price}</TableCell>
                  <TableCell>{item.distance}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </CardContent>
    </Card>
  );
}

export default MarketPriceTable;