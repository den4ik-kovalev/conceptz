Private Sub Worksheet_BeforeDoubleClick(ByVal Target As Range, Cancel As Boolean)
If Not Application.Intersect(Target, Range("B:B")) Is Nothing Then
    exe = ThisWorkbook.Path & "\" & "conceptz.exe"
    xls = ThisWorkbook.Path & "\" & ThisWorkbook.Name
    template = "template.html"
    key = CHR(34) & "Concept Name" & CHR(34)
    value = CHR(34) & Target & CHR(34)
    groupby = CHR(34) & "Section" & CHR(34)
    cmd = exe & " " & xls & " -t " & template & " -k " & key & " -v " & value & " -g " & groupby
    Call Shell(cmd)
End If
End Sub