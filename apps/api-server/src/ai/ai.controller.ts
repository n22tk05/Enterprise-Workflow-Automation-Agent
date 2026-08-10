import { Body, Controller, Post } from "@nestjs/common";
import { AiService } from "./ai.service";



@Controller("ai")
export class AiController {
    constructor(private readonly aiService: AiService) {}

    @Post('chat')
    async chat(@Body() body: any) {
        return await this.aiService.askAi(body.message, body.threadId)
    }
}
