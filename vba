Private Sub Worksheet_BeforeDoubleClick(ByVal Target As Range, Cancel As Boolean)
If Not Application.Intersect(Target, Range("B:B")) Is Nothing Then
    exe = ThisWorkbook.Path & "\" & "conceptz.exe"
    xls = ThisWorkbook.Path & "\" & ThisWorkbook.Name
    template = "concept.html"
    value = CHR(34) & Target & CHR(34)
    cmd = exe & " " & xls & " --template " & template & " --concept " & value
    Call Shell(cmd)
End If
End Sub