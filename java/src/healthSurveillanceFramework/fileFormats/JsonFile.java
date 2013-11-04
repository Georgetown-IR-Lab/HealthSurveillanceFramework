package healthSurveillanceFramework.fileFormats;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.IOException;
import java.io.FileReader;

import com.json.generators.JSONGenerator;
import com.json.generators.JsonGeneratorFactory;
import com.json.parsers.JSONParser;
import com.json.parsers.JsonParserFactory;

public abstract class JsonFile {
    JSONParser parser;
    JSONGenerator generator;

    protected JsonFile() {
        JsonParserFactory jpf = JsonParserFactory.getInstance();
        parser = jpf.newJsonParser();

        JsonGeneratorFactory jgf = JsonGeneratorFactory.getInstance();
        generator = jgf.newJsonGenerator();
    }

    abstract void loadJson(String filename);

    abstract void writeJson(String filename);

    public String readFile(String filename) {
        StringBuffer sb = new StringBuffer();

        try {
            BufferedReader br = new BufferedReader(new FileReader(filename));
            String line;
            while ((line = br.readLine()) != null) {
                sb.append(line);
                sb.append("\n");
            }
        } catch (IOException e) {
            System.err.println(e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }

        return sb.toString();
    }

    public void writeFile(String txt, String filename) {
        try {
            BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(filename), "utf-8"));
            writer.write(txt);
            writer.close();
        } catch (IOException e) {
            System.err.println(e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
}
