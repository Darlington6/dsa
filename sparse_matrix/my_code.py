class SparseMatrix:
    def __init__(self, matrix_file_path=None, num_rows=None, num_cols=None):
        if matrix_file_path:
            self._load_from_file(matrix_file_path)
        else:
            self.num_rows, self.num_cols = num_rows, num_cols
            self.rows = [{} for _ in range(self.num_rows)]

    def _load_from_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
                self.num_rows, self.num_cols = int(lines[0].split('=')[1]), int(lines[1].split('=')[1])
                self.rows = [{} for _ in range(self.num_rows)]
                for line in lines[2:]:
                    r, c, v = map(int, line[1:-1].split(','))
                    self.set_element(r, c, v)
        except (FileNotFoundError, PermissionError, OSError, ValueError) as e:
            raise e

    def set_element(self, row, col, value):
        if value != 0:
            self.rows[row][col] = value
        elif col in self.rows[row]:
            del self.rows[row][col]

    def add(self, other):
        return self._element_wise_operation(other, lambda a, b: a + b)

    def subtract(self, other):
        return self._element_wise_operation(other, lambda a, b: a - b)

    def multiply(self, other):
        if self.num_cols != other.num_rows:
            raise ValueError("Invalid dimensions for multiplication")
        result = SparseMatrix(num_rows=self.num_rows, num_cols=other.num_cols)
        other_col = [{} for _ in range(other.num_cols)]
   
    # Populate other_col
        for r in range(other.num_rows):
            for c, v in other.rows[r].items():
                if c < len(other_col):
                    other_col[c][r] = v
            else:
                print(f"Index out of range when populating other_col: c={c}, r={r}")
   
    # Perform multiplication
        for r in range(self.num_rows):
            for c, v in self.rows[r].items():
                if c < len(other_col):
                    for c_other, v_other in other_col[c].items():
                        result.set_element(r, c_other, result.get_element(r, c_other) + v * v_other)
            else:
                print(f"Index out of range when accessing other_col: c={c}, r={r}")
   
        return result

    def _element_wise_operation(self, other, op):
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)
        for r in range(self.num_rows):
            for c, v in self.rows[r].items():
                result.set_element(r, c, v)
        if r < len(other.rows):
            for c, v in other.rows[r].items():
                result.set_element(r, c, op(result.get_element(r, c), v))
        else:
            print(f"Index out of range: r={r}, len(other.rows)={len(other.rows)}")
        return result

    def get_element(self, row, col):
        return self.rows[row].get(col, 0)

    def write_to_file(self, file_path):
        try:
            with open(file_path, 'w') as f:
                f.write(f"rows={self.num_rows}\ncols={self.num_cols}\n")
                for r in range(self.num_rows):
                    for c, v in self.rows[r].items():
                        f.write(f"({r},{c},{v})\n")
        except (FileNotFoundError, PermissionError, OSError) as e:
            raise e

    def display(self):
        for r in range(self.num_rows):
            for c, v in self.rows[r].items():
                print(f"({r}, {c}, {v})", end=' ')
            print()

def main():
    try:
        choice = int(input("Enter operation: 1-Addition, 2-Subtraction, 3-Multiplication: ").strip())
        file1, file2 = input("Enter first matrix file: ").strip(), input("Enter second matrix file: ").strip()
        mat1, mat2 = SparseMatrix(matrix_file_path=file1), SparseMatrix(matrix_file_path=file2)

        if choice == 1:
            result = mat1.add(mat2)
        elif choice == 2:
            result = mat1.subtract(mat2)
        elif choice == 3:
            result = mat1.multiply(mat2)
        else:
            raise ValueError("Invalid choice")

        output_file = input("Enter output file path: ").strip()
        result.write_to_file(output_file)
        print(f"Operation completed. Result written to {output_file}.")
    except (ValueError, FileNotFoundError, PermissionError, OSError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()